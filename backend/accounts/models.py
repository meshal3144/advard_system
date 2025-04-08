from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.text import slugify

# نموذج الشركة
class Company(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass  # ليست هناك حاجة لتحديد `app_label`

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while Company.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


# نموذج المستخدم المخصص
class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'مدير النظام'),
        ('employee', 'موظف شركة'),
        ('manager', 'مدير شركة'),
        ('staff', 'موظف داخلي'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="الاسم الكامل")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)


    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,  # ✅ استخدم النموذج الصحيح من Django
        related_name="custom_user_groups",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,  # ✅ استخدم النموذج الصحيح أيضًا
        related_name="custom_user_permissions",
        blank=True
    )

    class Meta:
        pass  # إزالة `app_label` لأنه غير ضروري

    def __str__(self):
        return self.full_name or self.username
