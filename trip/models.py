from django.contrib.auth.models import User
from django.db import models

from common import ChoiceArrayField
from constants import TRAVEL_TYPE


# Create your models here.
class Trip(models.Model):
    destination_city = models.CharField(max_length=500, verbose_name="Destination City")
    destination_country = models.CharField(
        max_length=500, verbose_name="Destination Country"
    )

    class Meta:
        unique_together = ["destination_country", "destination_city"]


class UserTrip(models.Model):
    start_trip = models.DateField(
        verbose_name="Trip Start Date",
        help_text="Enter the date you will arrive at your destination",
    )
    end_trip = models.DateField(
        verbose_name="Trip End Date",
        help_text="Enter the date you plan to leave your destination",
    )
    travel_type = ChoiceArrayField(
        models.CharField(max_length=30, choices=TRAVEL_TYPE), default=list
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
