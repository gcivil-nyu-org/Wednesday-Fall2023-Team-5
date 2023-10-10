from django.db.models.signals import post_save
from .models import CustomUser, UserProfile
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def auto_create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()
