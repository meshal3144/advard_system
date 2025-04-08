from django import forms
from .models import InquiryRequest
class InquiryRequestForm(forms.ModelForm):
    class Meta:
        model = InquiryRequest
        fields = ['full_name', 'company_name', 'job_title', 'employees_count', 'email', 'phone']  # شيل request_type



