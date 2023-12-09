import datetime
import logging

from django.db import models
from enum import Enum

from chat.models import Thread
from trip.models import UserTrip
from user_profile.models import User


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
            sender_two = User.objects.get(id=self.receiver.id)
            t = Thread.objects.filter(first_user_id=sender.id)
            u = Thread.objects.filter(first_user_id=sender_two.id)
            if not t and not u:
                Thread.objects.create(
                    first_user=self.sender,
                    second_user=self.receiver,
                    updated=datetime.datetime.utcnow(),
                )

            print(t)
        elif self.match_status == MatchStatusEnum.UNMATCHED.value:
            sender = User.objects.get(id=self.sender.id)
            sender_two = User.objects.get(id=self.receiver.id)
            t = Thread.objects.filter(first_user_id=sender.id)
            u = Thread.objects.filter(first_user_id=sender_two.id)
            if t:
                print(t)
                t.delete()
            if u:
                print(u)
                u.delete()
            print("Deleting thread if unmatched")
        return super().save(*args, **kwargs)
