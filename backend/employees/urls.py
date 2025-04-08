from django.urls import path
from django.views.i18n import set_language  # ✅ الحل الصحيح هنا
from . import views
from .views import login_view


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_conditions, name='terms_conditions'),
    path('contact/', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),
    path('login/', login_view, name='login'),
    


    # مسار صفحة الخدمات
    path('services/', views.services, name='services'),

    # المسارات الفرعية لكل خدمة
path('services/attendance-system/', views.attendance_system, name='attendance_system'),
path('services/leave-system/', views.leave_system, name='leave_system'),
path('services/employee-info-system/', views.employee_info_system, name='employee_info_system'),
path('services/payroll-system/', views.payroll_system, name='payroll_system'),
path('services/performance-evaluation-system/', views.performance_evaluation_system, name='performance_evaluation_system'),
path('services/recruitment-system/', views.recruitment_system, name='recruitment_system'),
path('services/employee-self-service/', views.employee_self_service, name='employee_self_service'),
path('services/smart-reports/', views.smart_reports, name='smart_reports'),
path('services/work-environment-system/', views.work_environment_system, name='work_environment_system'),
path('services/workflow-approvals/', views.workflow_approvals, name='workflow_approvals'),
path('services/business-travel/', views.business_travel, name='business_travel'),
]




