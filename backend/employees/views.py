from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import CustomUser as User
from django.contrib.auth import get_user_model
from django.utils.translation import activate






def home(request):
    activate('ar')  # أو 'en' حسب رغبتك
    return render(request, 'home.html')

def about_us(request):
    activate('ar')
    return render(request, 'about.html')

def privacy_policy(request):
    activate('ar')
    return render(request, 'privacy.html')

def terms_conditions(request):
    activate('ar')
    return render(request, 'terms.html')

def contact(request):
    activate('ar')
    return render(request, 'contact.html')

def pricing(request):
    activate('ar')
    return render(request, 'pricing.html')

# عرض صفحة الخدمات المقدمة
def services(request):
    activate('ar')
    return render(request, 'services.html')

# عرض تفاصيل الخدمات الفرعية

def attendance_system(request):
    activate('ar')
    return render(request, 'services/attendance-system.html')

def leave_system(request):
    activate('ar')
    return render(request, 'services/leave-system.html')

def employee_info_system(request):
    return render(request, 'services/employee-info-system.html')

def payroll_system(request):
    activate('ar')
    return render(request, 'services/payroll-system.html')

def performance_evaluation_system(request):
    activate('ar')
    return render(request, 'services/performance-evaluation-system.html')

def recruitment_system(request):
    activate('ar')
    return render(request, 'services/recruitment-system.html')

def employee_self_service(request):
    activate('ar')
    return render(request, 'services/employee-self-service.html')

def smart_reports(request):
    activate('ar')
    return render(request, 'services/smart-reports.html')

def work_environment_system(request):
    return render(request, 'services/work-environment-system.html')

def workflow_approvals(request):
    activate('ar')
    return render(request, 'services/workflow-approvals.html')

def business_travel(request):
    activate('ar')
    return render(request, 'services/business-travel.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()  # تنظيف الإدخال لمنع الأخطاء الناتجة عن المسافات الزائدة
        password = request.POST.get('password', '')  # استخدم .get() لتجنب الأخطاء في حالة عدم إرسال البيانات
        print(request.POST)  # لمعرفة ما يتم إرساله بالفعل من النموذج


        if not email or not password:
            return render(request, 'login.html', {'error': 'يرجى إدخال البريد الإلكتروني وكلمة المرور.'})

        try:
            user = User.objects.get(email=email)  # البحث عن المستخدم المرتبط بالبريد
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'البريد الإلكتروني غير مسجل. يرجى التحقق.'})

        # استخدام المصادقة للتحقق من صحة البريد وكلمة المرور مباشرةً
        user = authenticate(request, username=user.username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')  # توجيه المستخدم إلى لوحة التحكم بعد نجاح تسجيل الدخول
        else:
            return render(request, 'login.html', {'error': 'كلمة المرور غير صحيحة. حاول مرة أخرى.'})

    return render(request, 'login.html')


def forgot_password_view(request):
    return render(request, 'forgot-password.html')

def reset_password_view(request):
    return render(request, 'reset-password.html')

def reset_success_view(request):
    return render(request, 'reset-success.html')

# ✅ صفحة لوحة التحكم محمية بـ @login_required
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

# ✅ صفحة الملف الشخصي محمية بـ @login_required (كمثال إذا لديك صفحة بروفايل)
@login_required
def profile_view(request):
    return render(request, 'profile.html')



@login_required
def profile_view(request):
    user = request.user  # جلب بيانات المستخدم المسجل حاليًا
    context = {
        'user_avatar': user.avatar.url if user.avatar else '/static/images/default_avatar.jpg',  # رابط الصورة
        'full_name': user.get_full_name() or user.username,  # الاسم الكامل أو اسم المستخدم
        'phone': user.phone,  # رقم الهاتف
        'email': user.email,  # الايميل
    }
    return render(request, 'employees/profile.html', context)  # غير اسم القالب حسب اسم ملفك