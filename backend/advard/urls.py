from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # لوحة إدارة Django
    path('admin/', admin.site.urls),

    # الموقع الرسمي (الواجهة العامة)
    path('', include('website.urls')),  # هذا بديل لـ employees القديم

    # لوحة الإدارة
    path('admin-panel/', include(('admin_panel.urls', 'admin_panel'), namespace='admin_panel')),


    # لوحة العميل
    path('client/', include('client_panel.urls')),

    # الحسابات: login, reset, set_password, إلخ
    path('accounts/', include('accounts.urls', namespace='accounts')),


    # تسجيل الخروج
    path('logout/', LogoutView.as_view(), name='logout'),

    # لوحة الطلبات الواردة
    path('requests/', include('requests.urls')),  # ✅ ربط التطبيق

    #   تطبيق العقود
    path('contracts/', include('contracts.urls')),



]

# ملفات الميديا
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

