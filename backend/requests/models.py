from django.db import models

class InquiryRequest(models.Model):
    REQUEST_TYPES = [
        ('trial', 'طلب عرض تجريبي'),
        ('pricing', 'طلب عرض سعر'),
    ]

    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('approved', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]

    full_name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    company_name = models.CharField(max_length=100, verbose_name="اسم الشركة")
    job_title = models.CharField(max_length=100, verbose_name="المسمى الوظيفي")
    employees_count = models.PositiveIntegerField(verbose_name="عدد الموظفين")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, verbose_name="رقم الجوال")
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES, verbose_name="نوع الطلب")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="الحالة")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")
    rejection_note = models.TextField(null=True, blank=True, verbose_name="سبب الرفض")
    quote_link = models.URLField(null=True, blank=True, verbose_name="رابط عرض السعر")

    def __str__(self):
        return f"{self.full_name} - {self.get_request_type_display()}"

    class Meta:
        verbose_name = "طلب اشتراك"
        verbose_name_plural = "الطلبات"
