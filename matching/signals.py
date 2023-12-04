import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.models import Thread
from .models import UserTripMatches, MatchStatusEnum


@receiver(post_save, sender=UserTripMatches)
def auto_create_threads(sender, instance, created, **kwargs):
    logger = logging.getLogger()
    if created:
        if instance.match_status == MatchStatusEnum.MATCHED.value:
            Thread.objects.get_or_create(instance.sender.id, instance.receiver.id)
            logger.info(
                "Creating new thread between "
                + instance.sender
                + " && "
                + instance.receiver
            )
        else:
            logger.info("Not a MATCHED status record")
    else:
        pass
