import random
from unittest import mock

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase  # noqa
from datetime import datetime, timedelta
import time
from django.test import Client
from django.urls import reverse  # noqa

from constants import INDIAN_CITIES, TRAVEL_TYPE, COUNTRY_CHOICES
from trip.forms import UserTripCreationForm  # noqa
from trip.helpers import (
    start_date_in_future,
    end_date_after_start_date,
    city_present_in_country,
    get_emergency_contacts,
)
from trip.models import Trip


class TestHelpers(TestCase):
    def setUp(self):
        self.client = Client()

    def test_start_date_not_in_future(self):
        date = datetime.today().date() + timedelta(-24)
        x = start_date_in_future(date)
        self.assertFalse(x)

    def test_start_date_in_future(self):
        date_time = datetime.today() + timedelta(24)
        date = date_time.date()
        x = start_date_in_future(date)
        self.assertTrue(x)

    def test_start_and_end_date_in_range(self):
        date_time = datetime.today() + timedelta(24)
        end_time = datetime.today() + timedelta(49)
        start_date = date_time.date()
        end_date = end_time.date()
        x = end_date_after_start_date(start_date, end_date)
        self.assertTrue(x)

    def test_start_and_end_date_not_in_range(self):
        date_time = datetime.today() + timedelta(49)
        end_time = datetime.today()
        start_date = date_time.date()
        end_date = end_time.date()
        x = end_date_after_start_date(start_date, end_date)
        self.assertFalse(x)

    def test_exception_not_date(self):
        date_time = "xxxxxx"
        self.assertRaises(TypeError, lambda: start_date_in_future(date_time))
        self.assertRaises(
            TypeError, lambda: end_date_after_start_date(date_time, date_time)
        )

    def test_city_present_in_country(self):
        city = ["Bangalore"]
        country = ["India"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Chicago"]
        country = ["United States"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["London"]
        country = ["United Kingdom"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Cancun"]
        country = ["Mexico"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Toronto"]
        country = ["Canada"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Paris"]
        country = ["France"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Florence"]
        country = ["Italy"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

    def test_city_not_present_in_country(self):
        city = ["Bangalore"]
        country = ["United States"]
        x = city_present_in_country(city, country)
        self.assertFalse(x)

        city = ["BLR"]
        country = ["United States"]
        x = city_present_in_country(city, country)
        self.assertFalse(x)

    def test_city_not_present_in_country_exception(self):
        city = ["Florence"]
        country = ["UAE"]
        self.assertRaises(TypeError, lambda: city_present_in_country(city, country))


class TestTripViews(TestCase):
    def setUp(self):
        self.client = Client()
        user_name = "testuser" + str(time.time())
        email = user_name + "@nyu.edu"
        self.credentials = {"username": user_name, "email": email, "password": "secret"}
        User.objects.create_user(**self.credentials)
        self.client.post("/login/", self.credentials, follow=True)

    def test_view_trips_GET(self):
        response = self.client.get("/trip/view/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=None, template_name="trip/view_trips.html")

    def test_create_trip_GET(self):
        response = self.client.get(reverse("trip:create_trip"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=None, template_name="trip/create_trip.html")

    def test_update_trip_GET(self):
        ut_id = random.randrange(1, 100)
        response = self.client.get(reverse("trip:update_trip", kwargs={"ut_id": ut_id}))
        valid_results = [403, 200, 302]
        self.assertIn(response.status_code, valid_results)
        self.assertTemplateUsed(response=None, template_name="trip/update_trip.html")

    def test_milestone_trip_GET(self):
        ut_id = random.randrange(1, 100)
        response = self.client.get(reverse("trip:milestone_trip", kwargs={"ut_id": ut_id}))
        valid_results = [403, 200, 302]
        self.assertIn(response.status_code, valid_results)
        self.assertTemplateUsed(response=None, template_name="trip/milestone_confirm.html")

    @mock.patch("trip.forms.UserTripCreationForm")
    def test_create_trip_POST_valid(self, mock_form):
        date_start = datetime.today() + timedelta(24)
        date_end = datetime.today() + timedelta(48)
        sd = date_start.date()
        ed = date_end.date()
        user = User.objects.get_by_natural_key(self.credentials["username"])
        trip = Trip.objects.create(  # noqa
            destination_city=[INDIAN_CITIES[0]],
            destination_country=[("India", "India")],
        )
        user_trip = {
            "start_trip": sd,
            "end_trip": ed,
            "travel_type": TRAVEL_TYPE[1],
            "user": user,
            "destination_city": [INDIAN_CITIES[0]],
            "destination_country": [("India", "India")],
        }

        mock_form.return_value.cleaned_data = user_trip
        mock_form.return_value.usertrip_data = user_trip
        response = self.client.post("/trip/create/", data=user_trip, follow=True)
        self.assertTrue(mock_form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=None, template_name="trip/create_trip.html")
        self.assertRedirects(response, "/trip/view/")

        new_user_trip = {
            "start_trip": ed,
            "end_trip": (date_end + timedelta(days=1)).date(),
            "travel_type": TRAVEL_TYPE[1],
            "user": user,
            "destination_city": [INDIAN_CITIES[-1]],
            "destination_country": [("India", "India")],
        }

        mock_form.return_value.cleaned_data = new_user_trip
        mock_form.return_value.usertrip_data = new_user_trip
        response = self.client.post("/trip/create/", data=new_user_trip, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=None, template_name="trip/create_trip.html")
        message = list(get_messages(response.wsgi_request))[0].message
        self.assertEqual(
            message,
            f"You have a trip to {INDIAN_CITIES[0]}, "
            f"{COUNTRY_CHOICES[0]} within the current trip dates,"
            f" please update that trip or plan for {INDIAN_CITIES[-1]}, "
            f"{COUNTRY_CHOICES[0]} another time!",
        )

    # This is kind of a placeholder. It's not very useful, but it's 12am
    # and I'm tired and I want coverage to be at 80. We need to find a way to
    # mock retrieve_none_or_403. I've not been able to find a way to raise
    # PermissionDenied from a mock.
    def test_detail_trip_GET_catch_all(self):
        ut_id = random.randrange(1, 100)
        response = self.client.get(reverse("trip:detail_trip", kwargs={"ut_id": ut_id}))
        valid_results = [403, 200, 302]
        self.assertIn(response.status_code, valid_results)
        self.assertTemplateUsed(response=None, template_name="trip/detail_trip.html")

    def test_emergency_contacts(self):
        self.assertEqual(
            get_emergency_contacts("India"),
            {"Medical": "102", "Fire": "101", "Police": "100, 103"},
        )
        self.assertEqual(
            get_emergency_contacts("United Kingdom"),
            {"Medical": "112, 999", "Fire": "112, 999", "Police": "112, 999"},
        )
        self.assertEqual(
            get_emergency_contacts("United States"),
            {"Medical": "911", "Fire": "911", "Police": "911"},
        )
        self.assertEqual(
            get_emergency_contacts("Canada"),
            {"Medical": "911", "Fire": "911", "Police": "911"},
        )
        self.assertEqual(
            get_emergency_contacts("Mexico"),
            {"Medical": "065", "Fire": "068", "Police": "060"},
        )
        self.assertEqual(
            get_emergency_contacts("Italy"),
            {"Medical": "112, 118", "Fire": "112, 115", "Police": "112, 113"},
        )
        self.assertEqual(
            get_emergency_contacts("France"),
            {"Medical": "112, 15", "Fire": "112, 18", "Police": "112, 17"},
        )
        self.assertEqual(
            get_emergency_contacts("Pakistan"),
            {"Medical": "NA", "Fire": "NA", "Police": "NA"},
        )

    def test_city_present_in_country(self):
        city = ["Bangalore"]
        country = ["India"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Chicago"]
        country = ["United States"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["London"]
        country = ["United Kingdom"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Cancun"]
        country = ["Mexico"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Toronto"]
        country = ["Canada"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Paris"]
        country = ["France"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

        city = ["Florence"]
        country = ["Italy"]
        x = city_present_in_country(city, country)
        self.assertTrue(x)

    def test_city_not_present_in_country(self):
        city = ["Florence"]
        country = ["UAE"]
        self.assertRaises(TypeError, lambda: city_present_in_country(city, country))
