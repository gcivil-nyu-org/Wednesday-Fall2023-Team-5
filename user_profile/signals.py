import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def auto_create_profile(sender, instance, created, **kwargs):
    logger = logging.getLogger()
    if created:
        UserProfile.objects.create(user=instance)
    else:
        logger.info("Profile created")


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    logger = logging.getLogger()
    instance.userprofile.save()
    logger.info("User Profile saved")
