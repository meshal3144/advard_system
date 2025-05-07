from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.models import CustomUser, Company, ClientUser, InternalEmployee
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from requests.models import InquiryRequest  # ← إذا التطبيق اسمه requests
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from contracts.models import CompanyContract, Company
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from accounts.signals import create_user_profile
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import get_connection
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from contracts.models import CompanyContract, SubscriptionPlan
import uuid  # ضعها في أعلى الملف إن لم تكن موجودة






@require_POST
@csrf_exempt
def mark_welcome_shown(request):
    if request.method == 'POST':
        request.session['welcome_shown'] = True
        request.session.modified = True  # تأكيد حفظ التغيير
        request.session.set_expiry(86400)  # انتهاء الجلسة بعد 24 ساعة (اختياري)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def dashboard_view(request):
    # لا تقم بتعيين welcome_shown هنا مطلقاً
    context = {
        'welcome_shown': request.session.get('welcome_shown', False)
    }
    return render(request, "admin_panel/dashboard.html", context)


def service_requests_view(request):
    requests = InquiryRequest.objects.all()

    # ✅ فلترة حسب نوع الطلب
    request_type = request.GET.get('type')
    if request_type:
        requests = requests.filter(request_type=request_type)

    # ✅ فلترة حسب الحالة
    status = request.GET.get('status')
    if status:
        requests = requests.filter(status=status)

    # ✅ فلترة حسب الاسم أو الشركة
    query = request.GET.get('q')
    if query:
        requests = requests.filter(full_name__icontains=query) | requests.filter(company_name__icontains=query)

    return render(request, "admin_panel/service_requests.html", {"requests": requests})



@login_required
def reports_page(request):
    return render(request, "admin_panel/dashboard.html")



@login_required
def clients_view(request):
    q = request.GET.get("q")
    status = request.GET.get("status")  

    clients = ClientUser.objects.select_related("user", "user__company").all()

    # ✅ فلترة حسب الاسم أو البريد أو الشركة
    if q:
        clients = clients.filter(
            Q(user__full_name__icontains=q) |
            Q(user__email__icontains=q) |
            Q(user__company__name__icontains=q)  
        )

    # ✅ فلترة حسب الحالة (مفعل / غير مفعل)
    if status:
        if status == "active":
            clients = clients.filter(user__is_active=True)
        elif status == "inactive":
            clients = clients.filter(user__is_active=False)

    context = {
        "clients": clients,
        "query": q,
        "status": status
    }

    return render(request, "admin_panel/clients.html", context)



@login_required
def client_detail_view(request, user_id):
    client = get_object_or_404(ClientUser.objects.select_related("user"), user__id=user_id)
    
    company = client.user.company if hasattr(client.user, 'company') else None  # جلب بيانات الشركة إذا كانت موجودة

    context = {
        "client": client,
        "company": company
    }

    return render(request, "admin_panel/client_detail.html", context)



@login_required
def view_request_detail(request, request_id):
    req = get_object_or_404(InquiryRequest, id=request_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '').strip()
        msg_content = ""

        # ✅ تضمين الملاحظات في الإيميل
        if note:
            msg_content += f"ملاحظات: {note}\n\n"

        

        if action == 'approve':
            req.status = 'approved'


            if req.request_type == 'trial':
                clean_name = req.company_name.strip()

                # 1️⃣ إنشاء أو جلب الشركة
                company, created = Company.objects.get_or_create(
                    name=clean_name,
                    defaults={
                                "company_code": f"{clean_name[:3].upper()}-{Company.objects.count() + 1}",
                                "contact_name": req.full_name,
                                "contact_phone": req.phone,
                                "city": "غير محدد",
                                "field": "غير محدد",
                            }
                        )


                # 2️⃣ توليد اسم مستخدم تلقائي
                email = req.email.strip().lower()

                # تحقق إذا المستخدم موجود مسبقًا بالبريد
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, ' هذا البريد الإلكتروني مسجل مسبقًا في النظام')
                    return redirect('admin_panel:service_requests')

                # استخدم البريد فقط بدون username


                # 3️⃣ التحقق من وجود المستخدم
                if CustomUser.objects.filter(email=req.email).exists():
                    messages.error(request, ' هذا البريد الإلكتروني مسجل مسبقًا في النظام')
                    return redirect('admin_panel:service_requests')



                # 4️⃣ إنشاء المستخدم
                user = CustomUser.objects.create(
                    email=email,
                    full_name=req.full_name,
                    phone=req.phone,
                    company=company,
                    is_active=False,
                    user_type='client',
                    national_id=f"temp-{uuid.uuid4().hex[:8]}"  # توليد رقم هوية مؤقت لتجاوز شرط unique
                )



                # 5️⃣ إنشاء ClientUser مرتبط
                ClientUser.objects.create(
                    user=user,
                    job_title=req.job_title,
                    employees_count=req.employees_count,
                )

                # 6️⃣ إنشاء اشتراك تجريبي
                if not hasattr(company, 'subscription'):
                    trial_plan = SubscriptionPlan.objects.filter(name__icontains="تجريبي").first()
                    if trial_plan:
                        CompanySubscription.objects.create(
                            company=company,
                            plan=trial_plan,
                            start_date=timezone.now().date(),
                            end_date=timezone.now().date() + timedelta(days=30),
                            is_active=True
                        )

                # 7️⃣ إنشاء رابط التعيين
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                domain = "advardsystem.com"  # ← هنا تم التثبيت
                registration_link = f"https://{domain}/accounts/set-password/{uid}/{token}/"

                msg_content += f"\nرابط التسجيل: {registration_link}"

            elif req.request_type == 'pricing':
                req.quote_link = request.POST.get('quote_link')
                msg_content += f"\nرابط عرض السعر: {req.quote_link}"

            req.save()

            subject = 'تم قبول طلبك – Advard'
            message = f"""عزيزي/ة {req.full_name},

يسعدنا إبلاغك بأنه قد تم قبول طلبك ({req.get_request_type_display()}).

{msg_content}

شكراً لثقتك بنا 🌟
"""
            send_mail(subject, message, None, [req.email]) 
            messages.success(request, '✔ تم قبول الطلب وإرسال البيانات')
            return redirect('admin_panel:service_requests')

        elif action == 'reject':
            req.status = 'rejected'
            req.rejection_note = note
            req.save()
            messages.warning(request, '✖ تم رفض الطلب')
            return redirect('admin_panel:service_requests')

    return render(request, 'admin_panel/service_request_detail.html', {
        'request_data': req
    })



@login_required
def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)  # ✅ استبدل `User` بـ `CustomUser`
    
    if request.method == "POST":
        user.full_name = request.POST.get("full_name")
        user.job_title = request.POST.get("job_title")
        user.national_id = request.POST.get("national_id")
        user.phone = request.POST.get("phone")
        user.role = request.POST.get("role")
        user.company_name = request.POST.get("company") 
        
        # ✅ تحديث الصورة الشخصية إذا تم رفعها
        if "avatar" in request.FILES:
            user.avatar = request.FILES["avatar"]

        user.save()
        messages.success(request, "تم تحديث بيانات المستخدم بنجاح!")
        return redirect("admin_panel:client_detail", user_id=user.id)

    return render(request, "admin_panel/client_edit.html", {"user": user})



# هنا دوال الارسال البريد دالتين

def send_real_html_email(to_email, context):
    html_content = render_to_string('accounts/password_reset_email.html', context)
    plain_content = strip_tags(html_content)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'إعادة تعيين كلمة المرور'
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = to_email

    # Attach plain and HTML
    msg.attach(MIMEText(plain_content, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # Open SMTP connection manually
    connection = get_connection()
    connection.open()
    connection.connection.sendmail(
        from_addr=settings.DEFAULT_FROM_EMAIL,
        to_addrs=[to_email],
        msg=msg.as_string()
    )
    connection.close()

    try:
        html_content = render_to_string('accounts/password_reset_email.html', context)
        plain_content = strip_tags(html_content)
    except Exception as e:
        print("⚠️ render_to_string failed:", str(e))
        raise



def send_set_password_link_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    context = {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'domain': 'advardsystem.com',  # ✳️ ثبّت اسم الدومين يدويًا
        'protocol': 'https',
        'site_name': 'Advard System'
    }

    send_real_html_email(user.email, context)
    messages.success(request, f"تم إرسال رابط تعيين كلمة المرور إلى {user.full_name}")
    return redirect('admin_panel:client_detail', user_id=user.id)







@login_required
def add_client_view(request):
    companies = Company.objects.all()

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        national_id = request.POST.get("national_id")
        job_title = request.POST.get("job_title")
        company_id = request.POST.get("company")

        if not all([email, full_name, phone, national_id]):
            messages.error(request, "❌ تأكد من تعبئة جميع الحقول المطلوبة.")
            return redirect("admin_panel:add_client")

        try:
            employees_count = int(request.POST.get("employees_count") or 0)
        except ValueError:
            employees_count = 0

        # التحقق من البريد ورقم الهوية
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "❌ البريد الإلكتروني مستخدم من قبل.")
            return redirect("admin_panel:add_client")

        if CustomUser.objects.filter(national_id=national_id).exists():
            messages.error(request, "❌ رقم الهوية مستخدم من قبل.")
            return redirect("admin_panel:add_client")

        # التحقق من الشركة
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            messages.error(request, "❌ الشركة المحددة غير موجودة.")
            return redirect("admin_panel:add_client")

        # التحقق إن الشركة لا تحتوي على مدير آخر
        if CustomUser.objects.filter(company=company, user_type="client_admin").exists():
            messages.error(request, "❌ هذه الشركة لديها مدير بالفعل ولا يمكن إضافة مدير آخر.")
            return redirect("admin_panel:add_client")


        try:
            # إنشاء المستخدم
            user = CustomUser.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                national_id=national_id,
                job_title=job_title,
                company=company,
                user_type="client_admin",
                is_active=False,
            )

            
            messages.success(request, f"✅ تم إضافة العميل {full_name} بنجاح!")
            return redirect("admin_panel:clients")

        except Exception as e:
            messages.error(request, f"❌ حدث خطأ أثناء الإضافة: {str(e)}")
            return redirect("admin_panel:add_client")

    return render(request, "admin_panel/add_client.html", {"companies": companies})


@login_required
def companies_list_view(request):
    companies = Company.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/companies.html', {'companies': companies})




@login_required
def add_company_view(request):
    # ✅ التقاط `next_action` من `POST` أو `GET`
    next_action = request.POST.get('next') or request.GET.get('next')

    if request.method == "POST":
        # ✅ التقاط بيانات النموذج مع إزالة المسافات الزائدة
        name = request.POST.get("name", "").strip()
        contact_name = request.POST.get("contact_name").strip()
        contact_phone = request.POST.get("contact_phone").strip()
        phone = request.POST.get("phone").strip()
        city = request.POST.get("city").strip()
        field = request.POST.get("field").strip()

        # ✅ إنشاء كود فريد للشركة
        company_code = f"{name[:3].upper()}-{Company.objects.count() + 1}"

        # ✅ حفظ بيانات الشركة الجديدة في قاعدة البيانات
        Company.objects.create(
            name=name,
            contact_name=contact_name,
            contact_phone=contact_phone,
            phone=phone,
            city=city,
            field=field,
            company_code=company_code
        )




        # ✅ إضافة رسالة نجاح
        messages.success(request, "تم حفظ الشركة بنجاح")

        # ✅ تنفيذ `redirect` بناءً على `next_action`
        if next_action == "add_contract":
            return redirect("contracts:add_contract")
        elif next_action == "add_client":
            return redirect("admin_panel:add_client")
        elif next_action == "companies":
            return redirect("admin_panel:companies")
        else:
            return redirect("admin_panel:companies")  # ✅ الرجوع الافتراضي إلى صفحة الشركات

    # ✅ عرض نموذج إضافة الشركة
    return render(request, "admin_panel/add_company.html")


@login_required
def company_detail_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, 'admin_panel/createcompany.html', {'company': company})



@login_required
def company_info_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    client = ClientUser.objects.filter(user__company=company, is_company_admin=True).first()


    return render(request, 'admin_panel/company_detail_info.html', {
        'company': company,
        'client': client
    })




@login_required
def delete_company_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        company.delete()
        messages.success(request, "✅ تم حذف الشركة بنجاح.")
        return redirect("admin_panel:companies")

    messages.error(request, "❌ لا يمكن حذف الشركة بهذه الطريقة.")
    return redirect("admin_panel:company_info", company_id=company_id)






@login_required
def edit_company_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    
    if request.method == "POST":
        try:
            company.name = request.POST.get("name", "")
            company.phone = request.POST.get("phone", "")
            company.city = request.POST.get("city", "")
            company.field = request.POST.get("field", "")
            company.contact_name = request.POST.get("contact_name", "")
            company.contact_phone = request.POST.get("contact_phone", "")
            company.save()
            
            messages.success(request, "✅ تم تحديث بيانات الشركة بنجاح.")
            return redirect('admin_panel:companies')
        except Exception as e:
            messages.error(request, f" حدث خطأ أثناء التحديث: {str(e)}")
            return redirect('admin_panel:edit_company', company_id=company.id)
    
    return render(request, 'admin_panel/createcompany.html', {"company": company})







@login_required
def panel_base_view(request):
    print("User Avatar:", user_avatar)
    user = request.user
    user_avatar = user.image.url if user.image and user.image.name else "/static/default-avatar.png"
    return render(request, "admin_panel/panel_base.html", {
        "user": user,
        "user_avatar": user_avatar,
        
    })
    

def employees_view(request):
    employees = InternalEmployee.objects.select_related('user').all()
    return render(request, 'admin_panel/employees.html', {'employees': employees})


# ✅ عرض تفاصيل موظف
def employee_detail_view(request, employee_id):
    employee = get_object_or_404(InternalEmployee, id=employee_id)
    return render(request, 'admin_panel/employee_detail.html', {'employee': employee})

def employee_add_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        national_id = request.POST.get('national_id')
        department = request.POST.get('department')
        job_title = request.POST.get('job_title')
        gender = request.POST.get('gender')
        nationality = request.POST.get('nationality')
        user_type = request.POST.get('user_type')
        role = request.POST.get('role')
        domain_verified = True if request.POST.get('domain_verified') == 'on' else False

        temp_password = get_random_string(8)
        employee_code = f"EMP-{get_random_string(4, allowed_chars='0123456789')}"

        if CustomUser.objects.filter(national_id=national_id).exists():
            messages.error(request, "رقم الهوية مستخدم مسبقًا")
            return redirect('admin_panel:employee_add')

        # ✅ قبل إنشاء المستخدم نفصل الـ signal
        post_save.disconnect(create_user_profile, sender=CustomUser)

        user = CustomUser.objects.create_user(
            email=email,
            password=temp_password,
            full_name=full_name,
            phone=phone,
            national_id=national_id,
            department=department,
            job_title=job_title,
            employee_code=employee_code,
            gender=gender,
            nationality=nationality,
            user_type=user_type,
            is_active=False,
            is_staff=True
        )

        # ✅ بعدها نعيد ربط الـ signal مرة ثانية
        post_save.connect(create_user_profile, sender=CustomUser)

        # ✅ نربط الموظف مباشرة
        InternalEmployee.objects.create(
            user=user,
            role=role,
            domain_verified=domain_verified
        )

        messages.success(request, f"تم إضافة الموظف بنجاح. كلمة المرور المؤقتة: {temp_password}")
        return redirect('admin_panel:employees')

    return render(request, 'admin_panel/employee_add.html')



# ✅ تعديل موظف
def employee_edit_view(request, employee_id):
    employee = get_object_or_404(InternalEmployee, id=employee_id)
    user = employee.user

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.national_id = request.POST.get('national_id')
        user.department = request.POST.get('department')
        user.job_title = request.POST.get('job_title')
        user.employee_code = request.POST.get('employee_code')
        user.gender = request.POST.get('gender')
        user.nationality = request.POST.get('nationality')
        user.user_type = request.POST.get('user_type')
        user.is_active = True if request.POST.get('is_active') == 'on' else False
        user.save()

        employee.role = request.POST.get('role')
        employee.domain_verified = True if request.POST.get('domain_verified') == 'on' else False
        employee.save()

        messages.success(request, "تم تحديث بيانات الموظف بنجاح")
        return redirect('admin_panel:employees')

    return render(request, 'admin_panel/employee_edit.html', {'employee': employee})

@login_required
def employee_delete_view(request, employee_id):
    user = get_object_or_404(CustomUser, id=employee_id)
    
    if request.method == "POST":
        user.delete()
        messages.success(request, " تم حذف الموظف بنجاح")
        return redirect('admin_panel:employees')  # تأكد أن هذا المسار يعمل
    
    messages.error(request, " لا يمكن تنفيذ الحذف بهذه الطريقة")
    return redirect('admin_panel:employees')




from contracts.views import contracts_list  # ✅ استدعاء القائمة الأساسية من تطبيق العقود

def contracts_list_view(request):
    return contracts_list(request)  # ✅ استدعاء الفيو مباشرة دون تكرار الكود



