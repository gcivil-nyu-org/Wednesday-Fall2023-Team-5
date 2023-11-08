from django import forms

from constants import CITY_CHOICES, COUNTRY_CHOICES
from .models import UserTrip
from django.core.exceptions import ValidationError
from .helpers import (
    start_date_in_future,
    end_date_after_start_date,
    city_present_in_country,
)


class UserTripCreationForm(forms.ModelForm):
    destination_city_ef = forms.MultipleChoiceField(
        choices=CITY_CHOICES, label="Destination City"
    )
    destination_country_ef = forms.MultipleChoiceField(
        choices=COUNTRY_CHOICES, label="Destination Country"
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get("start_trip")
        end_date = cleaned_data.get("end_trip")
        city = cleaned_data.get("destination_city_ef")
        country = cleaned_data.get("destination_country_ef")
        if not start_date_in_future(start_date):
            raise ValidationError("Start date must be in the future")
        if not end_date_after_start_date(start_date, end_date):
            raise ValidationError("End date must be after start date")
        if not city_present_in_country(city, country):
            raise ValidationError("City must be chosen from origin country")

        return cleaned_data

    class Meta:
        model = UserTrip
        fields = ("start_trip", "end_trip", "travel_type")
