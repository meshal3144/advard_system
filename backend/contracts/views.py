from datetime import datetime, date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from accounts.models import Company
from contracts.models import CompanyContract, SubscriptionPlan
from decimal import Decimal


# ✅ تفاصيل عقد محدد
def contract_detail_view(request, contract_id):
    contract = get_object_or_404(CompanyContract, pk=contract_id)
    return render(request, 'admin_panel/contract_detail.html', {'contract': contract})




def renew_contract(request, contract_id):
    contract = get_object_or_404(CompanyContract, id=contract_id)

    if request.method == "POST":
        renewal_duration = request.POST.get('renewal_duration')
        custom_end_date = request.POST.get('custom_end_date')
        notes = request.POST.get('notes')
        contract_file = request.FILES.get('contract_file')
        new_plan_id = request.POST.get('new_plan')
        discount_value = request.POST.get('discount_value')

        try:
            discount = Decimal(discount_value or 0)
        except:
            discount = Decimal(0)

        # ✅ نعتمد تاريخ نهاية العقد الحالي كبداية جديدة
        base_start = contract.end_date
        contract.renewed_start_date = base_start

        # ✅ تحديد تاريخ الانتهاء الجديد
        if renewal_duration == 'custom' and custom_end_date:
            try:
                contract.end_date = datetime.strptime(custom_end_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "تاريخ مخصص غير صالح.")
                return redirect('contracts:contract_detail', contract_id=contract.id)
        elif renewal_duration == '6':
            contract.end_date = base_start + timedelta(days=182)
        elif renewal_duration == '12':
            contract.end_date = base_start + timedelta(days=365)
        else:
            messages.error(request, "خيار مدة التجديد غير صحيح.")
            return redirect('contracts:contract_detail', contract_id=contract.id)

        contract.next_renewal_date = contract.end_date
        contract.last_renewal_date = datetime.today().date()
        contract.renewal_count += 1

        # ✅ إذا تم تغيير الباقة
        if new_plan_id and new_plan_id != str(contract.plan.id):
            contract.plan = get_object_or_404(SubscriptionPlan, id=new_plan_id)

        # ✅ ملاحظات وملف جديد
        if notes:
            contract.notes = notes
        if contract_file:
            contract.contract_file = contract_file

        # ✅ تحديث السعر بناءً على الباقة الجديدة
        employee_count = contract.employee_count or 0
        vat_percentage = contract.vat_percentage or Decimal(15.0)

        contract_cost = contract.plan.price_per_employee * employee_count
        final_amount = contract_cost - (contract_cost * discount)
        vat_amount = final_amount * (vat_percentage / 100)
        final_with_vat = final_amount + vat_amount

        contract.contract_cost = contract_cost
        contract.discount_value = discount
        contract.final_amount = final_amount
        contract.vat_amount = vat_amount
        contract.final_with_vat = final_with_vat

        contract.save()

        messages.success(request, f"تم تجديد عقد {contract.company.name} بنجاح!")
        return redirect('contracts:contract_detail', contract_id=contract.id)

    else:
        messages.error(request, "لا يمكنك الوصول لهذه الصفحة بهذه الطريقة.")
        return redirect('contracts:contract_detail', contract_id=contract.id)



# ✅ حذف العقد
def delete_contract_view(request, contract_id):
    contract = get_object_or_404(CompanyContract, id=contract_id)

    if request.method == "POST":
        contract.delete()
        messages.success(request, " تم حذف العقد بنجاح.")
        return redirect('contracts:contracts_list')  # غيّرها حسب اسم صفحة قائمة العقود

    messages.error(request, " لا يمكن حذف العقد بهذه الطريقة.")
    return redirect('admin_panel/contracts', contract_id=contract_id)





 # ✅ اضافة العقد
   
def create_contract(request):
    if request.method == "POST":
        try:
            company_id = request.POST.get('company')
            plan_id = request.POST.get('plan')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            terms = request.POST.get('terms')
            notes = request.POST.get('notes')
            contract_file = request.FILES.get('contract_file')
            signer_name = request.POST.get('signer_name')
            signer_email = request.POST.get('signer_email')
            signer_position = request.POST.get('signer_position')

            payment_method = request.POST.get('payment_method')
            payment_status = request.POST.get('payment_status')
            auto_renewal = request.POST.get('auto_renewal') == 'true'



            employee_count = int(request.POST.get('employee_count', 0))
            discount = Decimal(request.POST.get('discount_value', 0))
            vat_percentage = Decimal(request.POST.get('vat_percentage', 15.0))

            if not all([company_id, start_date, end_date]):
                messages.error(request, 'جميع الحقول المطلوبة يجب ملؤها.')
                return redirect('contracts:add_contract')

            company = get_object_or_404(Company, id=company_id)

            if CompanyContract.objects.filter(company=company, end_date__gte=date.today()).exists():
                messages.error(request, f"لا يمكن إضافة عقد جديد، يوجد عقد حالي فعال للشركة ({company.name}).")
                return redirect('contracts:add_contract')

            plan = None
            if plan_id:
                plan = get_object_or_404(SubscriptionPlan, id=plan_id)

            contract_cost = plan.price_per_employee * employee_count if plan else Decimal(0)
            final_amount = contract_cost - (contract_cost * discount)
            vat_amount = final_amount * (vat_percentage / 100)
            final_with_vat = final_amount + vat_amount

            contract = CompanyContract.objects.create(
                company=company,
                plan=plan,
                employee_count=employee_count,
                start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
                next_renewal_date=datetime.strptime(end_date, "%Y-%m-%d").date(),

                terms=terms,
                notes=notes,
                contract_file=contract_file,
                contract_cost=contract_cost,
                discount_value=discount,
                final_amount=final_amount,
                vat_percentage=vat_percentage,
                vat_amount=vat_amount,
                final_with_vat=final_with_vat,
                
                signer_name=signer_name,
                signer_email=signer_email,
                signer_position=signer_position,
                payment_method=payment_method,
                payment_status=payment_status,
                auto_renewal=auto_renewal
            )


            messages.success(request, '✅ تم إضافة العقد بنجاح.')
            return redirect('contracts:contracts_list')

        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء إنشاء العقد: {str(e)}')
            return redirect('contracts:add_contract')

    else:
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
    
    return render(request, 'admin_panel/contracts.html', {
        'contracts': contracts,
        'current_status': status,
        'search_query': search,
        'sort_by': sort
    })



