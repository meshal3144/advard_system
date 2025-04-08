from django.db import models

class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee_id = models.CharField(max_length=20, unique=True)  # رقم الموظف
    name = models.CharField(max_length=100)  # اسم الموظف
    email = models.EmailField(unique=True, null=True, blank=True)  # البريد الإلكتروني
    phone = models.CharField(max_length=15, null=True, blank=True)  # رقم الهاتف
    department = models.CharField(max_length=50)  # القسم
    job_title = models.CharField(max_length=50)  # المسمى الوظيفي
    date_joined = models.DateField(auto_now_add=True)  # تاريخ الانضمام

    def __str__(self):
        return f"{self.name} ({self.employee_id})"
