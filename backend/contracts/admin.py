from django.contrib import admin
from .models import CompanyContract

@admin.register(CompanyContract)
class CompanyContractAdmin(admin.ModelAdmin):

    list_display = ('company', 'contract_number', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('company__name', 'contract_number')

