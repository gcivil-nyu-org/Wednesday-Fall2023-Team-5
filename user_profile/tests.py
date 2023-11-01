# Create your tests here.
import sys
import time
from sys import argv
from unittest import TestCase

from django.contrib.auth.models import User
from django.test import SimpleTestCase


from django.urls import reverse
from django.test import Client


class TestUserProfile(TestCase):
    client = Client()
    def setUp(self):
        user_name = "testuser" + str(time.time())
        email = user_name + "@nyu.edu"
        self.credentials = {"username": user_name,
                            "email": email,
                            "password": "secret"}
        sys.argv = 'test'
        User.objects.create_user(**self.credentials)

    def test_login_view(self):
        response = self.client.get(reverse("user_profile:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        response = self.client.post("/login/", self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context["user"].is_active)
