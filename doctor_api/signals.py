from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import Doctor

@receiver(post_save, sender=CustomUser)
def create_doctor_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'Doctor':
        Doctor.objects.create(
            user=instance,
            specialty=instance.specialty or '',
            experience=0,  # Default value
            bio=''  # Default value
        )
