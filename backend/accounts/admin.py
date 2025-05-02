from django.contrib import admin
from .models import (
    CustomUser, Company, InternalEmployee,
    ClientUser, SubscriptionPlan, CompanySubscription
)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "user_type", "company", "is_active")
    search_fields = ("full_name", "email", "national_id")
    list_filter = ("user_type", "is_active", "company")
    autocomplete_fields = ["company"]

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "company_code", "contact_name", "city")
    search_fields = ("name", "company_code")

@admin.register(InternalEmployee)
class InternalEmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "domain_verified")
    autocomplete_fields = ["user"]

@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ("user", "role_in_company", "is_company_admin")
    autocomplete_fields = ["user"]

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "max_employees", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)  # ✅ هذا هو اللي كان ناقص


@admin.register(CompanySubscription)
class CompanySubscriptionAdmin(admin.ModelAdmin):
    list_display = ("company", "plan", "start_date", "end_date", "is_active")
    autocomplete_fields = ["company", "plan"]

