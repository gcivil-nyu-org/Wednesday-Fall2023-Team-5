# Create your tests here.
import time
from django.test import TestCase

from django.contrib.auth.models import User


from django.urls import reverse
from django.test import Client

from user_profile.helpers import email_is_valid


class TestUserProfile(TestCase):
    client = Client()

    def setUp(self):
        user_name = "testuser" + str(time.time())
        email = user_name + "@nyu.edu"
        self.credentials = {"username": user_name, "email": email, "password": "secret"}
        User.objects.create_user(**self.credentials)

    def test_login_view(self):
        response = self.client.get(reverse("user_profile:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_user(self):
        response = self.client.post("/login/", self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context["user"].is_active)

    def test_login_unknown_user(self):
        credentials = {
            "username": "unknown_user",
            "email": "unknown@nyu.edu",
            "password": "secret",
        }
        response = self.client.post("/login/", credentials, follow=True)
        # should be logged in now
        self.assertFalse(response.context["user"].is_active)

    def test_valid_email(self):
        email = "test@nyu.edu"
        x = email_is_valid(email)
        self.assertTrue(x)

    def test_in_valid_email(self):
        email = "123@nyu.edu"
        x = email_is_valid(email)
        self.assertFalse(x)

        email = "alpha"
        x = email_is_valid(email)
        self.assertFalse(x)

        email = "1233333333333333333333333@nyu.edu"
        x = email_is_valid(email)
        self.assertFalse(x)

class TestLoggedInViews(TestCase):

    def setUp(self):
        client = Client()
        user_name = "testuser" + str(time.time())
        email = user_name + "@nyu.edu"
        self.credentials = {"username": user_name, "email": email, "password": "secret"}
        User.objects.create_user(**self.credentials)
        self.client.post("/login/", self.credentials, follow=True)

    def test_milestone_profile_GET(self):
        response = self.client.get(reverse("user_profile:milestone_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/milestone_confirm.html')

    def test_milestone_profile_POST_delete_profile(self):
        user_instance = User.objects.get(username=self.credentials["username"])
        self.assertTrue(user_instance.is_active)
        response = self.client.post(reverse("user_profile:milestone_profile"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_default/home.html')
