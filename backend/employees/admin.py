from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'email', 'phone', 'department', 'job_title', 'date_joined')
    search_fields = ('name', 'employee_id', 'department')
    list_filter = ('department', 'job_title')
