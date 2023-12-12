import datetime
import logging

from django.db import models
from enum import Enum

from django.db.models import Q

from chat.models import Thread
from trip.models import UserTrip
from user_profile.models import User, UserImages


class MatchStatusEnum(Enum):
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    MATCHED = "Matched"
    UNMATCHED = "Unmatched"
    REJECTED = "Rejected"

    @classmethod
    def get_match_status(cls, value):
        if value == "Pending":
            return MatchStatusEnum.PENDING
        elif value == "Cancelled":
            return MatchStatusEnum.CANCELLED
        elif value == "Matched":
            return MatchStatusEnum.MATCHED
        elif value == "Unmatched":
            return MatchStatusEnum.UNMATCHED
        elif value == "Rejected":
            return MatchStatusEnum.REJECTED
        return None


class UserTripMatches(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_matches"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receive_matches"
    )
    sender_user_trip = models.ForeignKey(
        UserTrip, on_delete=models.CASCADE, related_name="sender_trip", null=True
    )
    receiver_user_trip = models.ForeignKey(
        UserTrip, on_delete=models.CASCADE, related_name="receiver_trip", null=True
    )

    MatchStatus = [
        (MatchStatusEnum.PENDING.value, MatchStatusEnum.PENDING.value),
        (MatchStatusEnum.CANCELLED.value, MatchStatusEnum.CANCELLED.value),
        (MatchStatusEnum.MATCHED.value, MatchStatusEnum.MATCHED.value),
        (MatchStatusEnum.UNMATCHED.value, MatchStatusEnum.UNMATCHED.value),
        (MatchStatusEnum.REJECTED.value, MatchStatusEnum.REJECTED.value),
    ]

    match_status = models.CharField(
        max_length=20, choices=MatchStatus, default=MatchStatusEnum.PENDING.value
    )

    def save(self, *args, **kwargs):
        logger = logging.getLogger()
        logger.info("In the save function Match status:")
        logger.info(self.match_status)
        if self.match_status == MatchStatusEnum.MATCHED.value:
            sender = User.objects.get(id=self.sender.id)
            receiver = User.objects.get(id=self.receiver.id)
            t = Thread.objects.filter(
                Q(first_user_id=sender.id) & Q(second_user_id=receiver.id)
            )
            u = Thread.objects.filter(
                Q(first_user_id=receiver.id) & Q(second_user_id=sender.id)
            )
            if not t and not u:
                sender_image = UserImages.objects.filter(
                    Q(user_profile_id=self.sender.id)
                )
                sender_image_url = ""
                receiver_image_url = ""
                sender_instances = [
                    UserImages(**item) for item in sender_image.values()
                ]
                if len(sender_instances) > 0:
                    sender_image_url = sender_instances[0].get_absolute_url()
                receiver_image = UserImages.objects.filter(
                    user_profile_id=self.receiver.id
                )
                receiver_instances = [
                    UserImages(**item) for item in receiver_image.values()
                ]
                if len(receiver_instances) > 0:
                    receiver_image_url = receiver_instances[0].get_absolute_url()
                Thread.objects.create(
                    first_user=self.sender,
                    second_user=self.receiver,
                    updated=datetime.datetime.utcnow(),
                    first_user_image_url=sender_image_url,
                    second_user_image_url=receiver_image_url,
                )

            print(t)
        elif self.match_status == MatchStatusEnum.UNMATCHED.value:
            sender = User.objects.get(id=self.sender.id)
            receiver = User.objects.get(id=self.receiver.id)
            t = Thread.objects.filter(
                Q(first_user_id=sender.id) & Q(second_user_id=receiver.id)
            )
            u = Thread.objects.filter(
                Q(first_user_id=receiver.id) & Q(second_user_id=sender.id)
            )
            if t:
                print(t)
                t.delete()
            if u:
                print(u)
                u.delete()
            print("Deleting thread if unmatched")
        return super().save(*args, **kwargs)
