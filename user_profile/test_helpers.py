import time

from django.test import TestCase

from django.contrib.auth.models import User


from django.urls import reverse
from django.test import Client


class TestLoggedInViews(TestCase):
    def setUp(self):
        client = Client()  # noqa
        user_name = "testuser" + str(time.time())
        email = user_name + "@nyu.edu"
        self.credentials = {"username": user_name, "email": email, "password": "secret"}
        User.objects.create_user(**self.credentials)
        self.client.post("/login/", self.credentials, follow=True)

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
