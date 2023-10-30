from django import forms
from .models import UserTrip


class UserTripCreationForm(forms.ModelForm):
    destination_city_ef = forms.CharField()
    destination_country_ef = forms.CharField()

    class Meta:
        model = UserTrip
        fields = ("start_trip", "end_trip", "travel_type")
