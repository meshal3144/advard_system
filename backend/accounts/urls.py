from django.urls import path
from .views import login_view, set_password_view
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = 'accounts'
from . import views



urlpatterns = [
    # تسجيل الدخول المخصص
    path('login/', login_view, name='login'),

    # صفحة إدخال البريد الإلكتروني (نسيت كلمة المرور)
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/forgot-password.html',  # الصفحة التي يدخل فيها البريد
        email_template_name='accounts/password_reset_email.html',  # قالب البريد الإلكتروني
        success_url=reverse_lazy('accounts:reset-requested')  # الانتقال لصفحة التأكيد بعد الإرسال
    ), name='forgot_password'),

    # صفحة تأكيد الإرسال (بعد إدخال البريد)
    path('reset-requested/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/reset-requested.html'  # صفحة "تم الإرسال"
    ), name='reset-requested'),

    # صفحة تعيين كلمة المرور الجديدة (الرابط الذي يصل بالإيميل)
    path('reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/reset-password.html',  # صفحة إدخال كلمة المرور الجديدة
        success_url=reverse_lazy('accounts:reset-success')  # الانتقال لصفحة النجاح
    ), name='password_reset_confirm'),

    # صفحة تأكيد نجاح التغيير
    path('reset-success/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/reset-success.html'  # صفحة "تم التغيير بنجاح"
    ), name='reset-success'),

    # المسار الإضافي الخاص بك (إذا كنت تحتاجه لوظيفة مختلفة)
    path('set-password/<uidb64>/<token>/', set_password_view, name='set_password'),

    path('reset-success/', views.reset_success_view, name='reset_success'),

    # صفحة لتفعيل المستخدم جديد

]
