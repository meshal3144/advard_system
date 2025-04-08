
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.contrib.auth import authenticate, login
from accounts.models import CustomUser
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser, Company
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404



User = get_user_model()

def set_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')

            if password == confirm_password and len(password) >= 8:
                user.set_password(password)
                user.save()
                login(request, user)
                messages.success(request, "تم تعيين كلمة المرور بنجاح 🎉")
                return redirect('dashboard')  # غيّرها حسب وجهتك الأساسية
            else:
                messages.error(request, "كلمة المرور غير متطابقة أو قصيرة جدًا.")
        return render(request, 'accounts/set_password.html')
    else:
        messages.error(request, "الرابط غير صالح أو انتهت صلاحيته.")
        return redirect('login')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # التحقق من وجود المستخدم
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # تسجيل الدخول ناجح
            login(request, user)
            return redirect('dashboard')
        else:
            # التحقق من سبب الفشل
            try:
                CustomUser.objects.get(email=email)
                # لو الايميل موجود بس كلمة المرور غلط
                messages.error(request, "كلمة المرور غير صحيحة")
            except CustomUser.DoesNotExist:
                # لو الايميل نفسه مش موجود
                messages.error(request, "البريد الإلكتروني غير موجود")
    
    # عرض الصفحة مع أي رسائل خطأ
    return render(request, 'employees/login.html')  # تأكد إن اسم القالب صحيح




@login_required
def profile_view(request):
    user = request.user

    context = {
        'user_avatar': user.avatar.url if user.avatar else '/static/images/default_avatar.jpg',
        'full_name': user.get_full_name() or user.username,
        'phone': user.phone,
        'email': user.email,
    }

    if request.method == 'POST':
        # تحديث رقم الجوال
        new_phone = request.POST.get('phone')
        if new_phone:
            user.phone = new_phone

        # رفع الصورة (اختياري)
        avatar = request.FILES.get('avatar')
        if avatar:
            user.avatar = avatar

        # تغيير كلمة المرور إذا كانت موجودة
        if request.POST.get('change_password'):
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not user.check_password(old_password):
                messages.error(request, 'كلمة المرور القديمة غير صحيحة.')
            elif new_password != confirm_password:
                messages.error(request, 'كلمة المرور الجديدة غير متطابقة.')
            elif len(new_password) < 8:
                messages.error(request, 'كلمة المرور قصيرة جدًا.')
            else:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                messages.success(request, 'تم تغيير كلمة المرور بنجاح ✅')

        user.save()
        messages.success(request, '✔ تم حفظ التغييرات بنجاح')
        return redirect('profile')

    return render(request, 'admin_panel/profile.html', context)


@csrf_exempt
def mark_welcome_shown(request):
    if request.method == 'POST':
        request.session['welcome_shown'] = True
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@login_required
def clients_view(request):
    q = request.GET.get('q')
    role = request.GET.get('role')

    users = CustomUser.objects.all()

    if q:
        users = users.filter(full_name__icontains=q) | users.filter(company__name__icontains=q)

    if role:
        users = users.filter(role=role)

    return render(request, 'admin_panel/clients.html', {'users': users})


@login_required
def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        # تحديث البيانات الأساسية
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.role = request.POST.get('role')
        company_id = request.POST.get('company')

        if company_id:
            user.company = Company.objects.get(id=company_id)

        # حفظ
        user.save()
        messages.success(request, '✅ تم تحديث بيانات المستخدم بنجاح')
        return redirect('clients')

    companies = Company.objects.all()
    return render(request, 'admin_panel/edit_user.html', {
        'user_obj': user,
        'companies': companies
    })



@login_required
def client_detail_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'admin_panel/client_detail.html', {'user': user})





# ✅ تفعيل المستخدم
@login_required
def activate_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        user.is_active = True
        user.save()
        messages.success(request, "✅ تم تفعيل المستخدم")
    return redirect('client_detail', user_id=user.id)

# ❌ تعطيل المستخدم
@login_required
def deactivate_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        user.is_active = False
        user.save()
        messages.warning(request, "❌ تم تعطيل المستخدم")
    return redirect('client_detail', user_id=user.id)

# ✉ إرسال رابط تعيين كلمة المرور
@login_required
def send_set_password_link_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        link = request.build_absolute_uri(
            reverse('set_password', kwargs={'uidb64': uid, 'token': token})
        )

        subject = "رابط تعيين كلمة المرور – Advard"
        message = f"""مرحبًا {user.get_full_name()},

تم إنشاء حسابك في نظام Advard بنجاح.
يرجى تعيين كلمة المرور الخاصة بك من خلال الرابط التالي:

{link}

⚠ ملاحظة: هذا الرابط صالح لفترة محدودة.

تحياتنا،
فريق Advard
"""
        send_mail(subject, message, None, [user.email])
        messages.success(request, "📩 تم إرسال رابط تعيين كلمة المرور إلى البريد الإلكتروني")

    return redirect('client_detail', user_id=user.id)




@login_required
def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    companies = Company.objects.all()

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.role = request.POST.get('role')
        company_id = request.POST.get('company')

        if company_id:
            user.company = Company.objects.get(id=company_id)

        avatar = request.FILES.get('avatar')
        if avatar:
            user.avatar = avatar

        user.save()
        messages.success(request, '✅ تم تحديث بيانات المستخدم بنجاح')
        return redirect('client_detail', user_id=user.id)

    return render(request, 'admin_panel/client_edit.html', {
        'user': user,
        'companies': companies
    })
