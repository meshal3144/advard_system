from django.contrib import admin
from .models import InquiryRequest

@admin.register(InquiryRequest)
class InquiryRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company_name', 'email', 'request_type', 'submitted_at')
    search_fields = ('full_name', 'email', 'company_name')




