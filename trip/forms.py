from cities_light.models import City, Country # noqa F401
from django import forms

from common import ChoiceArrayField # noqa F401
from constants import DEST_CITY, DEST_COUNTRY
from .models import UserTrip
from django.core.exceptions import ValidationError
from .helpers import start_date_in_future, end_date_after_start_date


class UserTripCreationForm(forms.ModelForm):
    destination_city_ef = forms.MultipleChoiceField(choices=DEST_CITY)
    destination_country_ef = forms.MultipleChoiceField(choices=DEST_COUNTRY)

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
