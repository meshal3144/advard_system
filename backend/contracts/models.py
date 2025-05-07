from django.db import models
from datetime import date, timedelta
from accounts.models import Company


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الباقة")
    max_employees = models.PositiveIntegerField(verbose_name="الحد الأقصى للموظفين")
    
    # ✅ تغيير وصف الحقل:
    price_per_employee = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="السعر لكل موظف (شهريًا)"
    )

    features = models.TextField(null=True, blank=True, verbose_name="المزايا")
    is_active = models.BooleanField(default=True, verbose_name="مفعّلة")

    def __str__(self):
        return f"{self.name} ({self.max_employees} موظف)"

    class Meta:
        verbose_name = "باقة اشتراك"
        verbose_name_plural = "باقات الاشتراك"


class CompanyContract(models.Model):
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('expiring', 'ينتهي قريباً'),
        ('expired', 'منتهي'),
        ('cancelled', 'ملغي'),
    ]

    PAYMENT_METHODS = [
        ('bank_transfer', 'تحويل بنكي'),
        ('credit_card', 'بطاقة ائتمان'),
        ('e_payment', 'دفع إلكتروني'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'مدفوع'),
        ('unpaid', 'غير مدفوع'),
        ('pending', 'قيد الانتظار'),
    ]

    contract_number = models.CharField(max_length=100, unique=True, verbose_name="رقم العقد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="الشركة")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الباقة")
    employee_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="عدد الموظفين")
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=15.0, verbose_name="نسبة ضريبة القيمة المضافة (%)")
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="قيمة الضريبة")
    final_with_vat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="الإجمالي شامل الضريبة")

    
    start_date = models.DateField(verbose_name="تاريخ البداية")
    end_date = models.DateField(verbose_name="تاريخ الانتهاء")

    renewed_start_date = models.DateField(null=True, blank=True, verbose_name="تاريخ بداية التجديد")
    last_renewal_date = models.DateField(null=True, blank=True, verbose_name="تاريخ التجديد الأخير")
    renewal_count = models.PositiveIntegerField(default=0, verbose_name="عدد مرات التجديد")
    next_renewal_date = models.DateField(null=True, blank=True, verbose_name="تاريخ التجديد القادم")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="الحالة")

    # 🔹 الحقول المالية
    contract_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="تكلفة العقد")
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="قيمة الخصم (نسبة %)")
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="الإجمالي بعد الخصم"
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True, blank=True, verbose_name="طريقة الدفع")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid', verbose_name="حالة الدفع")
    invoice_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="رقم الفاتورة")
    auto_renewal = models.BooleanField(default=False, verbose_name="تجديد تلقائي؟")

    # 🔹 بيانات الموقّع
    signer_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="اسم الموقّع")
    signer_email = models.EmailField(null=True, blank=True, verbose_name="البريد الإلكتروني للموقّع")
    signer_position = models.CharField(max_length=100, null=True, blank=True, verbose_name="الصفة الوظيفية للموقّع")

    terms = models.TextField(verbose_name="الشروط")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات إضافية")
    contract_file = models.FileField(upload_to='contracts/', null=True, blank=True, verbose_name="ملف العقد (اختياري)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")
    approved_by = models.CharField(max_length=255, null=True, blank=True, verbose_name="تمت الموافقة بواسطة")
    approval_date = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ الموافقة")



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

    def save(self, *args, **kwargs):
        today = date.today()

        # ✅ تحديث حالة العقد تلقائيًا
        if self.end_date < today:
            self.status = 'expired'
        elif self.end_date <= today + timedelta(days=15):
            self.status = 'expiring'
        else:
            self.status = 'active'

        # ✅ ضبط `next_renewal_date` فقط عند التجديد
        if self.renewal_count > 0:  # فقط إذا تم التجديد
            self.next_renewal_date = self.end_date  

                    # ✅ توليد رقم العقد تلقائيًا إذا لم يوجد
        if not self.contract_number:
            last_id = CompanyContract.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
            self.contract_number = f"CTR-{str(last_id + 1).zfill(6)}"

        # ✅ توليد رقم الفاتورة تلقائيًا إذا لم يوجد
        if not self.invoice_number:
            last_invoice = CompanyContract.objects.aggregate(max_inv=models.Max('id'))['max_inv'] or 0
            self.invoice_number = f"INV-{str(last_invoice + 1).zfill(6)}"


        super().save(*args, **kwargs)





    class Meta:
        verbose_name = "عقد شركة"
        verbose_name_plural = "عقود الشركات"



class ContractRenewalHistory(models.Model):
    contract = models.ForeignKey("CompanyContract", on_delete=models.CASCADE, related_name="renewals", verbose_name="العقد")
    renewal_date = models.DateField(auto_now_add=True, verbose_name="تاريخ التجديد")
    old_end_date = models.DateField(verbose_name="تاريخ النهاية السابق")
    new_end_date = models.DateField(verbose_name="تاريخ النهاية الجديد")
    notes = models.TextField(null=True, blank=True, verbose_name="ملاحظات")
    updated_by = models.CharField(max_length=255, verbose_name="تم التجديد بواسطة")  # لاحقًا يمكن ربطه بـ User

    class Meta:
        verbose_name = "تجديد عقد"
        verbose_name_plural = "سجل تجديدات العقود"
