from django.contrib.auth.models import User
from django.db import models

from common import ChoiceArrayField
from constants import TRAVEL_TYPE


# Create your models here.
class Trip(models.Model):
    destination_city = models.CharField(max_length=500)
    destination_country = models.CharField(max_length=500)
    travel_type = ChoiceArrayField(
        models.CharField(max_length=30, choices=TRAVEL_TYPE), default=list
    )


class UserTrip(models.Model):
    start_trip = models.DateTimeField("start_trip")
    end_trip = models.DateTimeField("end_trip")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
