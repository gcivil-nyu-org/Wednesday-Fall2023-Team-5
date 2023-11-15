from django.db import models
from enum import Enum

from trip.models import UserTrip
from user_profile.models import User


class MatchStatusEnum(Enum):
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    MATCHED = "Matched"
    UNMATCHED = "Unmatched"


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
    ]

    match_status = models.CharField(
        max_length=10, choices=MatchStatus, default=MatchStatusEnum.PENDING.value
    )
