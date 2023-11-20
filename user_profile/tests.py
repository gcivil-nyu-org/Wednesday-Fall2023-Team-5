# Create your tests here.
import time

# from unittest.mock import MagicMock

from faker import Faker
import datetime  # noqa
from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

from user_profile.helpers import email_is_valid, dob_gte18_and_lt100

# Testing View Functions


class TestLoginViews(TestCase):
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


class TestRegistrationViews(TestCase):
    def setUp(self):
        client = Client()  # noqa
        user_name = "testuser" + str(time.time())
        email = user_name + "@nyu.edu"
        self.credentials = {"username": user_name, "email": email, "password": "secret"}

    def test_create_user_account_GET(self):
        response = self.client.get(reverse("user_profile:register_account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile/user_registration.html")

    # @mock.patch("user_profile.forms.AccountRegistrationForm")
    # def test_create_user_account_POST_valid(self, mock_form):
    #     first_name = "Test"
    #     last_name = "User"
    #     username = self.credentials["username"]
    #     password = self.credentials["password"]
    #     email = self.credentials["email"]
    #
    #     mf_clean = {
    #         "first_name": first_name,
    #         "last_name": last_name,
    #         "username": username,
    #         "password1": password,
    #         "email": email,
    #     }
    #
    #     mock_form.return_value.cleaned_data = mf_clean
    #     #MagicMock(authenticate)
    #     # mock_form.return_value.authenticate =
    #
    #     response = self.client.post(
    #         reverse("user_profile:register_account"), data=mf_clean, follow=True
    #     )
    #
    #     self.assertTrue(mock_form.is_valid())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(
    #         response=None, template_name="user_profile/user_registration.html"
    #     )
    #     self.assertRedirects(response, reverse("user_profile:login"))


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

    @mock.patch("user_profile.forms.ProfileUpdateForm")
    def test_edit_profile_POST(self, mock_form):
        dob = datetime.date.today() - datetime.timedelta(days=365.25 * 20)
        uni = "NYU"
        age_lb = 18
        age_ub = 25
        drink_pref = [("Socially", "Socially")]
        smoke_pref = [("Socially", "Socially")]
        edu_level = [("In college", "In college")]
        interests = [("hiking", "hiking")]
        lang = [("English", "English")]

        mf_clean = {
            "dob": dob,
            "university": uni,
            "age_lower": age_lb,
            "age_upper": age_ub,
            "drink_pref": drink_pref,
            "smoke_pref": smoke_pref,
            "edu_level": edu_level,
            "interests": interests,
            "languages": lang,
        }

        mock_form.return_value.cleaned_data = mf_clean

        response = self.client.post(
            reverse("user_profile:edit_profile"), data=mf_clean, follow=True
        )

        self.assertTrue(mock_form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response=None, template_name="user_profile/edit_profile.html"
        )
        self.assertRedirects(response, reverse("user_profile:view_profile"))

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


# Testing Helper Functions


class TestHelperFunctions(TestCase):
    def setUp(self):
        self.fake = Faker()
        Faker.seed(2433)

    # Testing email validator
    def test_email_is_valid_valid(self):
        emails = ["test@nyu.edu", "mikey12@harvard.edu", "mz1233@princeton.edu"]
        for email in emails:
            x = email_is_valid(email)
            self.assertTrue(x)

    def test_email_is_valid_invalid_numeric(self):
        emails = ["123@nyu.edu", "alpha", "1233333333333333@nyu.edu"]
        for email in emails:
            x = email_is_valid(email)
            self.assertFalse(x)

    def test_email_is_valid_invalid_non_edu(self):
        emails = [
            "alpha@gmail.com",
            "beta@yahoo.com",
            "chi@whitehouse.gov",
            "delta@d.net",
        ]
        for email in emails:
            x = email_is_valid(email)
            self.assertFalse(x)

    # Testing dob_gte18_and_lt100
    def test_dob_gte18_and_lt100_valid(self):
        dob = self.fake.date_between(start_date="-99y", end_date="-18y")
        res = dob_gte18_and_lt100(dob)
        self.assertTrue(res[0])

    def test_dob_gte18_and_lt100_invalid_too_young(self):
        dob = self.fake.date_between(start_date="-17y", end_date="+100y")
        res = dob_gte18_and_lt100(dob)
        self.assertFalse(res[0])

    def test_dob_gte18_and_lt100_invalid_too_old(self):
        dob = self.fake.date_between(
            start_date=datetime.date(1, 1, 1), end_date="-100y"
        )
        res = dob_gte18_and_lt100(dob)
        self.assertFalse(res[0])
