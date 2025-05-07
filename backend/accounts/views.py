from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if hasattr(user, 'clientuser'):
                return redirect('client_dashboard')
            elif hasattr(user, 'internalemployee'):
                return redirect('admin_panel:dashboard')  
            else:
                messages.error(request, "لا توجد صلاحية مرتبطة بالحساب.")
                return redirect('accounts:login')

        else:
            try:
                User.objects.get(email=email)
                messages.error(request, "كلمة المرور غير صحيحة")
            except User.DoesNotExist:
                messages.error(request, "البريد الإلكتروني غير موجود")

    return render(request, 'accounts/login.html')




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
                user.is_active = True  # ✅ تفعيل الحساب بعد تعيين كلمة المرور
                user.save()                
                return redirect('accounts:reset_success')
            else:
                messages.error(request, "كلمة المرور غير متطابقة أو قصيرة جدًا.")
        return render(request, 'accounts/reset-password.html')  # ✅ هذا هو الصح
    else:
        messages.error(request, "الرابط غير صالح أو انتهت صلاحيته.")
        return redirect('accounts:login')



def reset_success_view(request):
    return render(request, 'accounts/reset-success.html')





@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        if "change_password" in request.POST:
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # مهم عشان ما يخرجك من الجلسة
                    messages.success(request, "✅ تم تغيير كلمة المرور بنجاح!")
                else:
                    messages.error(request, "⚠️ كلمة المرور الجديدة غير متطابقة!")
            else:
                messages.error(request, "⚠️ كلمة المرور القديمة غير صحيحة!")

        else:
            phone = request.POST.get("phone")
            email = request.POST.get("email") or user.email

            user.phone = phone
            user.email = email

            if "avatar" in request.FILES:
                user.image = request.FILES["avatar"]

            user.save()
            messages.success(request, "✅ تم حفظ التعديلات بنجاح!")

    return render(request, "admin_panel/profile.html", {
        "user": user,
        "user_avatar": user.image.url if user.image else "/static/images/default_avatar.svg",
        "phone": user.phone,
        "email": user.email,
    })