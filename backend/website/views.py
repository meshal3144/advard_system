from django.shortcuts import render
from django.utils.translation import activate
from django.contrib import messages


def home(request):
    activate('ar')  # أو 'en' حسب رغبتك
    return render(request, 'website/home.html')

def about_us(request):
    activate('ar')
    return render(request, 'website/about.html')

def privacy_policy(request):
    activate('ar')
    return render(request, 'website/privacy.html')

def terms_conditions(request):
    activate('ar')
    return render(request, 'website/terms.html')

def contact(request):
    activate('ar')
    return render(request, 'website/contact.html')

def pricing(request):
    activate('ar')
    return render(request, 'website/pricing.html')

# عرض صفحة الخدمات المقدمة
def services(request):
    activate('ar')
    return render(request, 'website/services.html')


# عرض تفاصيل الخدمات الفرعية

def attendance_system(request):
    activate('ar')
    return render(request, 'website/services/attendance-system.html')

def leave_system(request):
    activate('ar')
    return render(request, 'website/services/leave-system.html')

def employee_info_system(request):
    return render(request, 'website/services/employee-info-system.html')

def payroll_system(request):
    activate('ar')
    return render(request, 'website/services/payroll-system.html')

def performance_evaluation_system(request):
    activate('ar')
    return render(request, 'website/services/performance-evaluation-system.html')

def recruitment_system(request):
    activate('ar')
    return render(request, 'website/services/recruitment-system.html')

def employee_self_service(request):
    activate('ar')
    return render(request, 'website/services/employee-self-service.html')

def smart_reports(request):
    activate('ar')
    return render(request, 'website/services/smart-reports.html')

def work_environment_system(request):
    return render(request, 'website/services/work-environment-system.html')

def workflow_approvals(request):
    activate('ar')
    return render(request, 'website/services/workflow-approvals.html')

def business_travel(request):
    activate('ar')
    return render(request, 'website/services/business-travel.html')


def public_request_page(request):
    return render(request, 'website/services.html.html')
