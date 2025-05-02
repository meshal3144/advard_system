from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ClientUser, InternalEmployee

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type in ['internal_admin', 'internal_employee']:
            if not hasattr(instance, 'internalemployee'):
                InternalEmployee.objects.create(
                    user=instance,
                    role='other',
                    domain_verified=True
                )
        elif instance.user_type in ['client_admin', 'client_employee']:
            if not hasattr(instance, 'clientuser'):
                ClientUser.objects.create(
                    user=instance,
                    role_in_company='employee',
                    is_company_admin=False,
                    job_title="",
                    employees_count=1
                )
