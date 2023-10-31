from django import forms
from .models import UserTrip
from django.core.exceptions import ValidationError
from .helpers import start_date_in_future, end_date_after_start_date


class UserTripCreationForm(forms.ModelForm):
    destination_city_ef = forms.CharField(label="Destination City")
    destination_country_ef = forms.CharField(label="Destination Country")

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get("start_trip")
        end_date = cleaned_data.get("end_trip")

        if not start_date_in_future(start_date):
            raise ValidationError("Start date must be in the future")
        if not end_date_after_start_date(start_date, end_date):
            raise ValidationError("End date must be after start date")

        return cleaned_data

    class Meta:
        model = UserTrip
        fields = ("start_trip", "end_trip", "travel_type")
