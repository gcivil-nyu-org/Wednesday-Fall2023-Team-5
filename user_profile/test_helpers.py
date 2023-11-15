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