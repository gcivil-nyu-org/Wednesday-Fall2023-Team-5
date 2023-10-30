from django import forms
from .models import UserTrip


class UserTripCreationForm(forms.ModelForm):
    destination_city_ef = forms.CharField(label="Destination City")
    destination_country_ef = forms.CharField(label="Destination Country")

    class Meta:
        model = UserTrip
        fields = ("start_trip", "end_trip", "travel_type")
