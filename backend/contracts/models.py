from django.db import models
from datetime import date
from accounts.models import Company, SubscriptionPlan  # تأكد أن هذه المستوردات صح

class CompanyContract(models.Model):
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('expiring', 'ينتهي قريباً'),
        ('expired', 'منتهي')
    ]

    contract_number = models.CharField(max_length=100, unique=True, verbose_name="رقم العقد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="الشركة")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الباقة")

    start_date = models.DateField(verbose_name="تاريخ البداية")
    end_date = models.DateField(verbose_name="تاريخ الانتهاء")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="الحالة")

    terms = models.TextField(verbose_name="الشروط")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات إضافية")  # 🔥 أضف هذا هنا

    contract_file = models.FileField(upload_to='contracts/', null=True, blank=True, verbose_name="ملف العقد (اختياري)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    def __str__(self):
        return f"عقد {self.contract_number} - {self.company.name}"

    @property
    def days_until_expiry(self):
        today = date.today()
        return (self.end_date - today).days

    @property
    def is_expiring_soon(self):
        return 0 <= self.days_until_expiry <= 15

    @property
    def is_expired(self):
        return self.end_date < date.today()

    class Meta:
        verbose_name = "عقد شركة"
        verbose_name_plural = "عقود الشركات"

