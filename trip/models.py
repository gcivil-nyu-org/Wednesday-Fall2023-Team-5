from django.contrib.auth.models import User
from django.db import models
from constants import TRAVEL_TYPE


# Create your models here.
class Trip(models.Model):
    destination_city = models.CharField(max_length=500, verbose_name="Destination City")
    destination_country = models.CharField(
        max_length=500, verbose_name="Destination Country"
    )

    def __str__(self):
        return f"DCT: {self.destination_city}, \
        DCTR: {self.destination_country}"

    # TripMetaData
    class Meta:
        """
        unique_together is an attribute that alters the way get_or_create
        interacts with the Trip model. With it set, get_or_create will
        consider destination_country and destination_city as a tuple when
        determining whether an entry is unique or not. This is important to
        ensure that multiple countries can share city names without being
        lumped in as the same place, and also so that cities in the same
        country are considered distinct destinations
        """

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
    travel_type = models.CharField(max_length=30, choices=TRAVEL_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"UserID: {self.user}, \
        TT: {self.travel_type}, \
        TripID: {self.trip}, \
        SD: {self.start_trip}, \
        ED: {self.end_trip}"
