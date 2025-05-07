from django.contrib import admin
from .models import InquiryRequest

@admin.register(InquiryRequest)
class InquiryRequestAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'company_name', 'request_type',
        'email', 'phone', 'status_display', 'submitted_at'
    )
    search_fields = ('full_name', 'company_name', 'email', 'phone')
    list_filter = ('request_type', 'status', 'submitted_at')
    readonly_fields = ('submitted_at',)
    list_per_page = 25

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'الحالة'
