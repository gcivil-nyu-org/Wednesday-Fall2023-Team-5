from django.test import TestCase  # noqa

# Create your tests here.
from datetime import datetime, timedelta

from trip.helpers import (
    start_date_in_future,
    end_date_after_start_date,
    city_present_in_country,
)


class TestTrip(TestCase):
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
