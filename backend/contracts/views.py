from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from contracts.models import CompanyContract
from datetime import datetime, timedelta

from django.db.models import Q
from datetime import date, timedelta
from django.http import JsonResponse
from accounts.models import Company  # استيراد الشركة
from contracts.models import CompanyContract, SubscriptionPlan  # استيراد العقود والباقات
from datetime import datetime


# ✅ عرض كل العقود
def contracts_list_view(request):
    contracts = CompanyContract.objects.all()
    return render(request, 'admin_panel/contracts.html', {'contracts': contracts})

# ✅ تفاصيل عقد محدد
def contract_detail_view(request, contract_id):
    contract = get_object_or_404(CompanyContract, pk=contract_id)
    return render(request, 'admin_panel/contract_detail.html', {'contract': contract})

# ✅ تجديد العقد

def renew_contract(request, contract_id):
    contract = get_object_or_404(CompanyContract, id=contract_id)

    if request.method == "POST":
        print("📦 DEBUG - POST DATA:", request.POST)
        print("📦 DEBUG - FILES DATA:", request.FILES)
        renewal_duration = request.POST.get('renewal_duration')
        custom_end_date = request.POST.get('custom_end_date')
        notes = request.POST.get('notes')
        contract_file = request.FILES.get('contract_file')

        print("🛠️ البيانات المستلمة:")
        print("renewal_duration:", renewal_duration)
        print("custom_end_date:", custom_end_date)
        print("notes:", notes)
        print("contract_file:", contract_file)

        if renewal_duration == 'custom' and custom_end_date:
            try:
                contract.end_date = datetime.strptime(custom_end_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "❌ تاريخ مخصص غير صالح.")
                return redirect('admin_panel:contract_detail', contract_id=contract.id)
        elif renewal_duration == '6':
            contract.end_date = contract.end_date + timedelta(days=182)
        elif renewal_duration == '12':
            contract.end_date = contract.end_date + timedelta(days=365)
        else:
            messages.error(request, "❌ خيار مدة التجديد غير صحيح.")
            return redirect('admin_panel:contract_detail', contract_id=contract.id)

        if notes:
            contract.notes = notes

        if contract_file:
            contract.contract_file = contract_file

        contract.save()

        messages.success(request, f"✅ تم تجديد عقد {contract.company.name} بنجاح!")
        return redirect('admin_panel:contract_detail', contract_id=contract.id)

    else:
        messages.error(request, "❌ لا يمكنك الوصول لهذه الصفحة بهذه الطريقة.")
        return redirect('admin_panel:contract_detail', contract_id=contract.id)





def create_contract(request):  # تغيير اسم الدالة
    if request.method == "POST":
        try:
            company_id = request.POST.get('company')
            contract_number = request.POST.get('contract_number')
            plan_id = request.POST.get('plan')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            terms = request.POST.get('terms')
            notes = request.POST.get('notes')
            contract_file = request.FILES.get('contract_file')

            # التحقق من الحقول المطلوبة
            if not all([company_id, contract_number, start_date, end_date]):
                messages.error(request, 'جميع الحقول المطلوبة يجب ملؤها')
                return redirect('contracts:add_contract')

            # جلب الشركة
            company = get_object_or_404(Company, id=company_id)

            # جلب الباقة إذا وجدت
            plan = None
            if plan_id:
                try:
                    plan = SubscriptionPlan.objects.get(id=plan_id)
                except SubscriptionPlan.DoesNotExist:
                    pass

            # إنشاء العقد
            contract = CompanyContract.objects.create(
                company=company,
                contract_number=contract_number,
                plan=plan,
                start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
                terms=terms,
                notes=notes,
                contract_file=contract_file
            )

            messages.success(request, 'تم إضافة العقد بنجاح')
            return redirect('contracts:contracts_list')

        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء إنشاء العقد: {str(e)}')
            return redirect('contracts:add_contract')
    
    else:
        # عرض صفحة الإضافة
        companies = Company.objects.all()
        plans = SubscriptionPlan.objects.all()
        return render(request, 'admin_panel/add_contract.html', {
            'companies': companies,
            'plans': plans
        })
    







def contracts_list(request):
    # جلب معايير الفلترة
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '-start_date')
    
    # استعلام أساسي
    contracts = CompanyContract.objects.all()
    
    # فلترة حسب الحالة
    today = date.today()
    if status == 'active':
        contracts = contracts.filter(start_date__lte=today, end_date__gte=today)
    elif status == 'expired':
        contracts = contracts.filter(end_date__lt=today)
    elif status == 'expiring_soon':
        soon = today + timedelta(days=30)
        contracts = contracts.filter(end_date__range=[today, soon])
    
    # فلترة بالبحث
    if search:
        contracts = contracts.filter(
            Q(company__name__icontains=search) |
            Q(contract_number__icontains=search)
        )
    
    # ترتيب النتائج
    if sort == 'start_date':
        contracts = contracts.order_by('start_date')
    elif sort == '-start_date':
        contracts = contracts.order_by('-start_date')
    elif sort == 'end_date':
        contracts = contracts.order_by('end_date')
    elif sort == '-end_date':
        contracts = contracts.order_by('-end_date')
    
    return render(request, 'contracts/contracts_list.html', {
        'contracts': contracts,
        'current_status': status,
        'search_query': search,
        'sort_by': sort
    })