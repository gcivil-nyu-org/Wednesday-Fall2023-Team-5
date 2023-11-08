from django.db import models

from trip.models import Trip
from user_profile.models import User


class UserTripMatches(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_matches"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receive_matches"
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    MatchStatus = [
        ("Pending", "Pending"),
        ("Cancelled", "Cancelled"),
        ("Matched", "Matched"),
        ("Unmatched", "Unmatched"),
    ]

    match_status = models.CharField(
        max_length=10, choices=MatchStatus, default="Pending"
    )
