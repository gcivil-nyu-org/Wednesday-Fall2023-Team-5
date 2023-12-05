from datetime import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from trip.models import UserTrip, Trip


class TestMatchingViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.password = 'matching_password'
        self.user1 = User.objects.create_user(
            username='matching_user',
            email='matching_user@nyu.edu',
            password=self.password,
        )
        self.user1.userprofile.dob = datetime(1997, 8, 22)
        self.user1.save()
        self.user2 = User.objects.create_user(
            username='matching_user2',
            email='matching_user2@nyu.edu',
            password=self.password
        )
        self.user2.userprofile.dob = datetime(1997, 8, 22)
        self.user2.save()
        self.user3 = User.objects.create_user(
            username='matching_user3',
            email='matching_user3@nyu.edu',
            password=self.password
        )
        self.user3.userprofile.dob = datetime(1997, 8, 22)
        self.user3.save()
        city = [('Bangalore', 'Bangalore')]
        country = [('India', 'India')]
        companion = ("Companion", "Companion")
        trip_destination = Trip.objects.create(
            destination_city=city,
            destination_country=country
        )
        self.utrip1 = UserTrip.objects.create(
            start_trip=datetime(2023, 12, 18),
            end_trip=datetime(2023, 12, 28),
            user=self.user1,
            travel_type=companion,
            trip=trip_destination,
        )
        self.utrip2 = UserTrip.objects.create(
            start_trip=datetime(2023, 12, 14),
            end_trip=datetime(2023, 12, 24),
            travel_type=companion,
            user=self.user2,
            trip=trip_destination,
        )
        self.utrip3 = UserTrip.objects.create(
            start_trip=datetime(2023, 12, 20),
            end_trip=datetime(2023, 12, 30),
            travel_type=companion,
            user=self.user3,
            trip=trip_destination,
        )

    def test_show_potential_matches(self):
        user1login = self.client.login(
            username='matching_user',
            password=self.password,
        )
        self.assertTrue(user1login)
        response = self.client.get(
            reverse("matching:show_potential_matches", kwargs={"utrip_id": self.utrip1.id})
        )
        matching_users = [mu['user'] for mu in response.context['matching_users']]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name="matching/list_potential_matches.html")
        self.assertNotIn(self.user1, matching_users)
        self.assertIn(self.user2, matching_users)
        self.assertIn(self.user3, matching_users)
        self.client.logout()

        user2login = self.client.login(
            username='matching_user2',
            password=self.password,
        )
        self.assertTrue(user2login)
        response = self.client.get(
            reverse("matching:show_potential_matches", kwargs={"utrip_id": self.utrip2.id})
        )
        matching_users = [mu['user'] for mu in response.context['matching_users']]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user1, matching_users)
        self.assertNotIn(self.user2, matching_users)
        self.assertIn(self.user3, matching_users)
        self.client.logout()

        user3login = self.client.login(
            username='matching_user3',
            password=self.password,
        )
        self.assertTrue(user3login)
        response = self.client.get(
            reverse("matching:show_potential_matches", kwargs={"utrip_id": self.utrip3.id})
        )
        matching_users = [mu['user'] for mu in response.context['matching_users']]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user1, matching_users)
        self.assertIn(self.user2, matching_users)
        self.assertNotIn(self.user3, matching_users)
