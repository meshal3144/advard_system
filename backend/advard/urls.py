from django.contrib import admin
from django.urls import path, include
from employees import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employees.urls')),  # ربط التطبيق بالصفحة الرئيسية
    path('login/', include('django.contrib.auth.urls')),  # مسار تسجيل الدخول الافتراضي
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('reset-success/', views.reset_success_view, name='reset_success'),
    path('inquiry/', include('admin_panel.urls')),
    path('', include('admin_panel.urls')),
    path('admin-panel/', include('admin_panel.urls')),  # مسارات لوحة الإدارة
    path('accounts/', include('accounts.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
