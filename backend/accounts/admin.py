from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'full_name', 'email', 'role', 'company', 'is_staff', 'is_superuser')
    list_filter = ('role', 'company', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('معلومات المستخدم', {
            'fields': ('full_name', 'email', 'phone', 'avatar', 'company', 'role')
        }),
        ('الصلاحيات', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('تواريخ الدخول', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'full_name', 'email'),
        }),
    )
