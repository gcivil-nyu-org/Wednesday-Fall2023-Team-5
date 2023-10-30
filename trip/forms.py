from django import forms
from .models import Trip, UserTrip


class TripCreationForm(forms.ModelForm):
    # Here, we can define a clean function and validate the
    # destination.

    class Meta:
        model = Trip
        fields = ("destination_country", "destination_city")


class UserTripCreationForm(forms.ModelForm):
    class Meta:
        model = UserTrip
        fields = ("start_trip", "end_trip", "travel_type")
