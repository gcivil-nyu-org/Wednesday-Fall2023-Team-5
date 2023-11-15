# Create your tests here.
import time
import datetime  # noqa
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
        client = Client()  # noqa
        user_name = "testuser" + str(time.time())
        email = user_name + "@nyu.edu"
        self.credentials = {"username": user_name, "email": email, "password": "secret"}
        User.objects.create_user(**self.credentials)
        self.client.post("/login/", self.credentials, follow=True)

    # Milestone profile coverage
    def test_milestone_profile_GET(self):
        response = self.client.get(reverse("user_profile:milestone_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile/milestone_confirm.html")

    def test_milestone_profile_POST_delete_profile(self):
        user_instance = User.objects.get(username=self.credentials["username"])
        self.assertTrue(user_instance.is_active)
        response = self.client.post(
            reverse("user_profile:milestone_profile"), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home_default/home.html")

    # Edit profile coverage
    def test_edit_profile_GET(self):
        response = self.client.get(reverse("user_profile:edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile/edit_profile.html")

    # View profile coverage
    def test_view_profile_GET(self):
        response = self.client.get(reverse("user_profile:view_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile/view_profile.html")

    # Detail profile coverage
    def test_detail_profile_GET_user_dne(self):
        # if the user does not exist in the database, we should be redirecting to home
        response = self.client.get(
            reverse("user_profile:detail_profile", kwargs={"id": 30000})
        )
        self.assertEqual(response.status_code, 302)

    def test_detail_profile_GET_user_exists(self):
        active_user = User.objects.get(username=self.credentials["username"])
        active_id = active_user.pk
        response = self.client.get(
            reverse("user_profile:detail_profile", kwargs={"id": active_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile/detail_profile.html")

    def test_detail_profile_GET_user_inactive(self):
        active_user = User.objects.get(username=self.credentials["username"])
        active_id = active_user.pk
        active_user.is_active = False
        active_user.save()
        response = self.client.get(
            reverse("user_profile:detail_profile", kwargs={"id": active_id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile/detail_profile_inactive.html")
