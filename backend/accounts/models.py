from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone



class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم الشركة")
    company_code = models.CharField(max_length=50, unique=True, verbose_name="المعرف الداخلي")
    contact_name = models.CharField(max_length=100, verbose_name="اسم المسؤول")
    contact_phone = models.CharField(max_length=20, verbose_name="رقم جوال المسؤول")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="هاتف الشركة")
    city = models.CharField(max_length=100, verbose_name="المدينة")
    field = models.CharField(max_length=100, verbose_name="مجال العمل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return f"{self.name} ({self.company_code})"

    class Meta:
        verbose_name = "شركة"
        verbose_name_plural = "الشركات"




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('البريد الإلكتروني مطلوب')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ('internal_admin', 'مسؤول داخلي'),
        ('internal_employee', 'موظف داخلي'),
        ('client_admin', 'مدير شركة عميلة'),
        ('client_employee', 'موظف شركة عميلة'),
    ]

    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    full_name = models.CharField(max_length=255, verbose_name="الاسم الكامل")
    phone = models.CharField(max_length=20, verbose_name="رقم الجوال")
    national_id = models.CharField(max_length=20, unique=True, verbose_name="رقم الهوية")
    gender = models.CharField(max_length=10, choices=[('male', 'ذكر'), ('female', 'أنثى')], null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True, verbose_name="الجنسية")
    job_title = models.CharField(max_length=100, null=True, blank=True, verbose_name="المسمى الوظيفي")
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name="القسم")
    employee_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="الرقم الوظيفي")
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='client_employee', verbose_name="نوع المستخدم")
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="الشركة التابع لها")
    image = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name="الصورة الشخصية")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'national_id']

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "المستخدم"
        verbose_name_plural = "المستخدمون"


class InternalEmployee(models.Model):
    ROLE_CHOICES = [
        ('admin', 'مسؤول نظام'),
        ('support', 'دعم فني'),
        ('sales', 'مندوب مبيعات'),
        ('other', 'أخرى'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="حساب المستخدم")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='other', verbose_name="الدور")
    domain_verified = models.BooleanField(default=False, verbose_name="تم التحقق من الدومين")

    def __str__(self):
        return f"{self.user.full_name} - {self.get_role_display()}"

    class Meta:
        verbose_name = "موظف داخلي"
        verbose_name_plural = "الموظفون الداخليون"


class ClientUser(models.Model):
    ROLE_CHOICES = [
        ('employee', 'موظف'),
        ('supervisor', 'مشرف'),
        ('admin', 'مدير الشركة'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="حساب المستخدم")
    role_in_company = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee', verbose_name="الدور داخل الشركة")
    is_company_admin = models.BooleanField(default=False, verbose_name="هل هو مدير الشركة؟")
    job_title = models.CharField(max_length=100, null=True, blank=True, verbose_name="المسمى الوظيفي")
    employees_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="عدد الموظفين")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    

    def __str__(self):
        return f"{self.user.full_name} - {self.get_role_in_company_display()}"

    class Meta:
        verbose_name = "موظف شركة عميلة"
        verbose_name_plural = "موظفو الشركات"

