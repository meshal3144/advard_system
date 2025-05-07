from django.contrib import admin
from .models import CompanyContract, SubscriptionPlan


@admin.register(CompanyContract)
class CompanyContractAdmin(admin.ModelAdmin):
    list_display = (
        'company', 'contract_number', 'plan', 'start_date', 'end_date',
        'status', 'payment_status', 'contract_cost', 'auto_renewal'
    )
    list_filter = (
        'status', 'payment_status', 'payment_method', 'auto_renewal',
        'start_date', 'end_date'
    )
    search_fields = ('company__name', 'contract_number', 'invoice_number')
    autocomplete_fields = ['company', 'plan']
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_employees', 'price_per_employee', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
