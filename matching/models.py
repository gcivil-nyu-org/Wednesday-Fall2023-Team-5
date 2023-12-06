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
            t, _ = Thread.objects.get_or_create(
                first_user=self.sender, second_user=self.receiver
            )
            print(t)
        return super().save(*args, **kwargs)
