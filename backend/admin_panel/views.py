from django.shortcuts import render, redirect, get_object_or_404
from .forms import InquiryRequestForm
from .models import InquiryRequest
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from accounts.models import CustomUser, Company
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required

def submit_request(request, request_type):
    if request.method == 'POST':
        print(request.POST)  # يعرض البيانات المرسلة في الـ terminal

        form = InquiryRequestForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.request_type = request_type  # تعيين نوع الطلب
            inquiry.save()
            return redirect('success_page')  # صفحة نجاح العملية
        else:
            return render(request, 'services.html', {'form': form, 'errors': form.errors})
    else:
        return render(request, 'services.html', {'form': InquiryRequestForm()})


def thank_you(request):
    return render(request, 'admin_panel/thank_you.html')


def reports_page(request):
    return render(request, 'admin_panel/dashboard.html')


def profile_view(request):
    return render(request, 'admin_panel/profile.html')


def service_requests_view(request):
    q = request.GET.get('q')
    req_type = request.GET.get('type')

    requests = InquiryRequest.objects.all()

    if q:
        requests = requests.filter(
            Q(full_name__icontains=q) |
            Q(company_name__icontains=q)
        )

    if req_type:
        requests = requests.filter(request_type=req_type)

    requests = requests.order_by('-submitted_at')

    return render(request, 'admin_panel/service_requests.html', {'requests': requests})


def view_request_detail(request, request_id):
    req = get_object_or_404(InquiryRequest, id=request_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        note = request.POST.get('note', '').strip()

        # قبول الطلب
        if action == 'approve':
            req.status = 'مقبول'

            msg_content = f"ملاحظات: {note}\n" if note else ""
            registration_link = ""

            if req.request_type == 'pricing':
                req.quote_link = request.POST.get('quote_link')
                req.save()
                msg_content += f"\nرابط عرض السعر: {req.quote_link}"

            elif req.request_type == 'trial':
                # إنشاء الشركة والمستخدم
                company = Company.objects.create(name=req.company_name)

                user = CustomUser.objects.create(
                    username=req.email.split('@')[0],
                    email=req.email,
                    full_name=req.full_name,
                    phone=req.phone,
                    company=company,
                    is_active=False  # سيتم تفعيله بعد تعيين كلمة المرور
                )







                # توليد رابط التعيين
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                registration_link = f"https://advard.sa/set-password/{uid}/{token}/"
                msg_content += f"\nرابط التسجيل: {registration_link}"

                req.save()

            # إرسال الإيميل
            subject = 'تم قبول طلبك – Advard'
            message = f"""عزيزي/ة {req.full_name},

يسعدنا إبلاغك بأنه قد تم قبول طلبك ({req.get_request_type_display()}).

{msg_content}

شكراً لثقتك بنا 🌟
"""

            send_mail(subject, message, None, [req.email])
            messages.success(request, '✔ تم قبول الطلب وإرسال الإيميل بنجاح')
            return redirect('service_requests')

        # رفض الطلب
        elif action == 'reject':
            req.status = 'مرفوض'
            req.rejection_note = note
            req.save()

            subject = 'تم رفض طلبك – Advard'
            message = f"""عزيزي/ة {req.full_name},

نأسف لإبلاغك بأن طلبك ({req.get_request_type_display()}) لم يتم قبوله في الوقت الحالي.

{f"سبب الرفض: {note}" if note else "سبب الرفض: غير مذكور"}

لأي استفسار، لا تتردد بالتواصل معنا.

تحياتنا،  
فريق Advard
"""

            send_mail(subject, message, None, [req.email])
            messages.warning(request, '✖ تم رفض الطلب وإرسال الإيميل بنجاح')
            return redirect('service_requests')

    return render(request, 'admin_panel/service_request_detail.html', {
        'request_data': req
    })



@login_required
def client_detail_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'admin_panel/client_detail.html', {'user': user})
