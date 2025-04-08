from django.db import models

class InquiryRequest(models.Model):
    REQUEST_TYPES = [
        ('trial', 'عرض تجريبي'),
        ('pricing', 'عرض سعر'),
    ]

    STATUS_CHOICES = [
        ('قيد المراجعة', 'قيد المراجعة'),
        ('مقبول', 'مقبول'),
        ('مرفوض', 'مرفوض'),
    ]

    full_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    employees_count = models.PositiveIntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='قيد المراجعة')
    submitted_at = models.DateTimeField(auto_now_add=True)
    rejection_note = models.TextField(null=True, blank=True)
    quote_link = models.URLField(null=True, blank=True, verbose_name="رابط عرض السعر")

