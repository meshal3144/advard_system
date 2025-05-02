from django.urls import path, include
from . import views
from django.conf.urls.i18n import set_language
from .views import add_client_view
from .views import panel_base_view
from accounts.views import profile_view
from .views import employee_delete_view

app_name = 'admin_panel'





urlpatterns = [
    path('contracts/', include('contracts.urls')),
    path('profile/', profile_view, name='profile'),
    path('set-language/', set_language, name='set_language'),
    path('clients/', views.clients_view, name='clients'),
    path('service-requests/', views.service_requests_view, name='service_requests'),
    path('service-requests/<int:request_id>/', views.view_request_detail, name='view_request_detail'),
    path('edit-user/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('send-set-password-link/<int:user_id>/', views.send_set_password_link_view, name='send_set_password_link'),
    path('add-client/', add_client_view, name='add_client'),  # ✅ إضافة مسار إنشاء العميل
    path('companies/add/', views.add_company_view, name='add_company'),
    path("panel-base/", panel_base_view, name="panel_base"),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # ✅ إضافة المسار الصحيح
    path('clients/<int:user_id>/', views.client_detail_view, name='client_detail'),
    #path('clients/<int:user_id>/edit/', views.edit_user_view, name='edit_user'),
    #path('clients/<int:user_id>/activate/', views.activate_user_view, name='activate_user'),
    #path('clients/<int:user_id>/deactivate/', views.deactivate_user_view, name='deactivate_user'),
    path('clients/<int:user_id>/send-link/', views.send_set_password_link_view, name='send_set_password_link'),
    path('accounts/', include('accounts.urls')),
    path('mark-welcome-shown/', views.mark_welcome_shown, name='mark_welcome_shown'),
    path('contracts/', include(('contracts.urls', 'contracts'), namespace='contracts')),
    path('contracts/<int:contract_id>/', views.contract_detail_view, name='contract_detail'),
    # عرض  جدول الموظفين
    path('employees/', views.employees_view, name='employees'),
    # عرض تفاصيل موظف
    path('employees/<int:employee_id>/', views.employee_detail_view, name='employee_detail'),

    # إضافة موظف جديد
    path('employees/add/', views.employee_add_view, name='employee_add'),

    # تعديل موظف
    path('employees/<int:employee_id>/edit/', views.employee_edit_view, name='employee_edit'),

    # حذف موظف    
    path('employees/<int:employee_id>/delete/', employee_delete_view, name='employee_delete'),

    path('companies/', views.companies_list_view, name='companies'),
    path('companies/<int:company_id>/edit/', views.edit_company_view, name='edit_company'),
    path('companies/<int:company_id>/', views.company_detail_view, name='company_detail'),





]


