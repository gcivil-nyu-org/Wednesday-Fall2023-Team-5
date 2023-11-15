# import json

from django.contrib.auth.models import User
from django.db.models import Choices
from django.test import TestCase  # noqa

# Create your tests here.
from datetime import datetime, timedelta
import time
from django.test import Client
from django.urls import reverse  # noqa

# from constants import TRAVEL_TYPE, INDIAN_CITIES
from trip.forms import UserTripCreationForm  # noqa
from trip.helpers import (
    start_date_in_future,
    end_date_after_start_date,
    city_present_in_country,
)

# from trip.models import UserTrip, Trip


class TestTrip(TestCase):
    def setUp(self):
        user_name = "testuser" + str(time.time())
        email = user_name + "@nyu.edu"
        self.credentials = {"username": user_name, "email": email, "password": "secret"}
        User.objects.create_user(**self.credentials)

    client = Client()

    def test_start_date_not_in_future(self):
        date = datetime.today().date()
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

    def test_view_trips(self):
        response = self.client.login(**self.credentials)
        response = self.client.get("/trip/view/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=None, template_name="trip/view_trips.html")

    # def test_user_trip_create_form(self):
    #     response = self.client.login(**self.credentials)
    #
    #     user = User.objects.get_by_natural_key(self.credentials["username"])
    #     trip = Trip.objects.create(
    #         destination_city=[INDIAN_CITIES[0]],
    #         destination_country=[("India", "India")],
    #     )
    #
    #     # user_trip = UserTrip.objects.create(
    #     #     start_trip=(datetime.today() + timedelta(24)).date,
    #     #     end_trip=(datetime.today() + timedelta(48)).date,
    #     #     travel_type=TRAVEL_TYPE[1],
    #     #     user=user,
    #     #     trip=trip,
    #     # )
    #     # print(json.dumps(user_trip))
    #     date_start = datetime.today() + timedelta(24)
    #     date_end = datetime.today() + timedelta(48)
    #     sd = date_start.date()
    #     ed = date_end.date()
    #     user_trip = {
    #         "start_trip": sd,
    #         "end_trip": ed,
    #         "travel_type": TRAVEL_TYPE[1],
    #         "user": user,
    #         "trip": trip,
    #     }
    #     print(user_trip)
    #     form = UserTripCreationForm(
    #         {
    #             "start_trip": sd,
    #             "end_trip": ed,
    #             "travel_type": TRAVEL_TYPE[1],
    #             "user": user,
    #             "trip": trip,
    #         }
    #     )
    #     # print(form.is_valid())
    #
    #     # response = self.client.post("/trip/create/", data=user_trip)
    #     # self.assertEqual(response.status_code, 200)
    #     # self.assertTemplateUsed(response=None, template_name="trip/view_trips.html")
