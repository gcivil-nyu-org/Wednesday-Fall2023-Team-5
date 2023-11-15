from django import forms

from constants import CITY_CHOICES, COUNTRY_CHOICES, TRAVEL_TYPE
from .models import UserTrip
from django.core.exceptions import ValidationError
from .helpers import (
    start_date_in_future,
    end_date_after_start_date,
    city_present_in_country,
)


class UserTripCreationForm(forms.ModelForm):
    travel_type = forms.ChoiceField(choices=TRAVEL_TYPE, widget=forms.RadioSelect())

    destination_country = forms.MultipleChoiceField(
        choices=COUNTRY_CHOICES,
        label="Destination Country",
        widget=forms.SelectMultiple(attrs={"id": "country-create-field"}),
    )

    destination_city = forms.MultipleChoiceField(
        choices=CITY_CHOICES,
        label="Destination City",
        widget=forms.SelectMultiple(attrs={"id": "city-create-field"}),
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get("start_trip")
        end_date = cleaned_data.get("end_trip")
        city = cleaned_data.get("destination_city")
        country = cleaned_data.get("destination_country")

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
        widgets = {
            "start_trip": forms.widgets.DateInput(attrs={"type": "date"}),
            "end_trip": forms.widgets.DateInput(attrs={"type": "date"}),
        }

    class Media:
        js = ["trip/js/form-conditional-display.js"]


class UserTripUpdateForm(forms.ModelForm):
    travel_type = forms.ChoiceField(choices=TRAVEL_TYPE, widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get("start_trip")
        end_date = cleaned_data.get("end_trip")
        if not start_date_in_future(start_date):
            raise ValidationError("Start date must be in the future")
        if not end_date_after_start_date(start_date, end_date):
            raise ValidationError("End date must be after start date")

    class Meta:
        model = UserTrip
        fields = ("start_trip", "end_trip", "travel_type")
        widgets = {
            "start_trip": forms.widgets.DateInput(attrs={"type": "date"}),
            "end_trip": forms.widgets.DateInput(attrs={"type": "date"}),
        }
