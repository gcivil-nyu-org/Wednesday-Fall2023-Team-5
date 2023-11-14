import sys

from django.test import TestCase  # noqa

# Create your tests here.
from datetime import datetime, timedelta

from trip.helpers import start_date_in_future, end_date_after_start_date


class TestTrip(TestCase):
    def setUp(self):
        sys.argv = "test"

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
        self.assertRaises(TypeError, lambda: end_date_after_start_date(date_time, date_time))
