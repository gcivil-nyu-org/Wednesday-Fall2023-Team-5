from datetime import datetime

from django.db.models import Q, QuerySet  # noqa
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from chat.models import Thread
from trip.models import UserTrip, Trip
from django.contrib.messages import get_messages


class TestMatchingViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "matching_password"
        self.user1 = User.objects.create_user(
            username="matching_user",
            email="matching_user@nyu.edu",
            password=self.password,
        )
        self.user1.userprofile.dob = datetime(1997, 8, 22)
        self.user1.save()
        self.user2 = User.objects.create_user(
            username="matching_user2",
            email="matching_user2@nyu.edu",
            password=self.password,
        )
        self.user2.userprofile.dob = datetime(1997, 8, 22)
        self.user2.save()
        self.user3 = User.objects.create_user(
            username="matching_user3",
            email="matching_user3@nyu.edu",
            password=self.password,
        )
        self.user3.userprofile.dob = datetime(1997, 8, 22)
        self.user3.save()
        city = [("Bangalore", "Bangalore")]
        country = [("India", "India")]
        companion = ("Companion", "Companion")
        trip_destination = Trip.objects.create(
            destination_city=city, destination_country=country
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
            username="matching_user",
            password=self.password,
        )
        self.assertTrue(user1login)
        response = self.client.get(
            reverse(
                "matching:show_potential_matches", kwargs={"utrip_id": self.utrip1.id}
            )
        )
        matching_users = [mu["user"] for mu in response.context["matching_users"]]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name="matching/list_potential_matches.html")
        self.assertNotIn(self.user1, matching_users)
        self.assertIn(self.user2, matching_users)
        self.assertIn(self.user3, matching_users)
        self.client.logout()
        user = self.client.session.get("_auth_user_id")
        self.assertIsNone(user)

        user2login = self.client.login(
            username="matching_user2",
            password=self.password,
        )
        self.assertTrue(user2login)
        response = self.client.get(
            reverse(
                "matching:show_potential_matches", kwargs={"utrip_id": self.utrip2.id}
            )
        )
        matching_users = [mu["user"] for mu in response.context["matching_users"]]
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user1, matching_users)
        self.assertNotIn(self.user2, matching_users)
        self.assertIn(self.user3, matching_users)

        response = self.client.get(
            reverse(
                "matching:show_potential_matches", kwargs={"utrip_id": self.utrip1.id}
            ),
            follow=True,
        )
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(template_name="trip/view_trips.html")
        self.client.logout()
        user = self.client.session.get("_auth_user_id")
        self.assertIsNone(user)

    def test_send_matching_request(self):
        user1login = self.client.login(
            username="matching_user",
            password=self.password,
        )
        self.assertTrue(user1login)
        response = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip1.id}),
            {"receiver_uid": self.user2.id, "receiver_utrip_id": self.utrip2.id},
            follow=True,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(messages)
        self.assertEqual(messages[0].message, "Matching request sent to user")
        resp_up = response.context["matching_users"]
        for mu in resp_up:
            if mu["user"] == self.user2:
                self.assertTrue(mu["sent_match"], False)
                break
        self.utrip2.is_active = False
        self.utrip2.save()
        response = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip1.id}),
            {"receiver_uid": self.user2.id, "receiver_utrip_id": self.utrip2.id},
            follow=True,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(
            messages[0].message, "The receiver or their trip is not active anymore."
        )
        self.client.logout()

        self.utrip2.is_active = True
        self.utrip2.save()
        user2login = self.client.login(
            username="matching_user2",
            password=self.password,
        )
        self.assertTrue(user2login)
        response = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip2.id}),
            {
                "receiver_uid": self.user1.id,
                "receiver_utrip_id": self.utrip1.id,
            },
            follow=True,
        )
        self.assertIn(response.status_code, [200, 302])
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(len(messages), 1)
        self.assertEqual(
            messages[0].message,
            "The receiver might already have sent a matching "
            "request to you, please check your pending matches",
        )
        response = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "receiver_uid": self.user1.id,
                "receiver_utrip_id": self.utrip1.id,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 403)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(len(messages), 1)
        self.assertEqual(
            messages[0].message,
            "You are not allowed to edit this.",
        )
        self.assertTemplateUsed(response=None, template_name="trip/view_trips.html")

    def test_cancel_matching_request(self):
        self.client.login(
            username="matching_user",
            password=self.password,
        )
        _ = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip1.id}),
            {"receiver_uid": self.user2.id, "receiver_utrip_id": self.utrip2.id},
            follow=True,
        )
        response = self.client.post(
            reverse("matching:cancel_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "receiver_uid": self.user2.id,
                "receiver_utrip_id": self.utrip2.id,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            messages[0].message, "Your matching request is cancelled successfully"
        )

        response = self.client.post(
            reverse("matching:cancel_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "receiver_uid": self.user2.id,
                "receiver_utrip_id": self.utrip2.id,
            },
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "Your matching request has already been cancelled.",
        )

        _ = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip1.id}),
            {"receiver_uid": self.user2.id, "receiver_utrip_id": self.utrip2.id},
            follow=True,
        )
        self.client.logout()
        self.client.login(
            username="matching_user2",
            password=self.password,
        )
        _ = self.client.post(
            reverse("matching:react_request", kwargs={"utrip_id": self.utrip2.id}),
            {
                "sender_utrip_id": self.utrip1.id,
                "sender_id": self.user1.id,
                "pending_request": "Rejected",
            },
            follow=True,
        )
        self.client.logout()
        self.client.login(
            username="matching_user",
            password=self.password,
        )
        response = self.client.post(
            reverse("matching:cancel_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "receiver_uid": self.user2.id,
                "receiver_utrip_id": self.utrip2.id,
            },
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "Your matching request might have already been responded, "
            "and hence cannot cancel anymore, "
            "please try to unmatch, if matched or "
            "try sending the request again",
        )

    def test_show_pending_requests(self):
        self.client.login(
            username="matching_user",
            password=self.password,
        )
        self.utrip1.is_active = False
        self.utrip1.save()
        response = self.client.get(
            reverse(
                "matching:show_pending_requests", kwargs={"utrip_id": self.utrip1.id}
            ),
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "The trip is not active anymore, cannot show pending request",
        )
        self.assertTemplateUsed(template_name="trip/view_trips.html")

    def test_react_pending_request(self):
        self.client.login(username="matching_user2", password=self.password)
        _ = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip2.id}),
            {
                "receiver_utrip_id": self.utrip1.id,
                "receiver_uid": self.user1.id,
            },
            follow=True,
        )
        self.client.logout()
        self.client.login(username="matching_user", password=self.password)
        self.utrip1.is_active = False
        self.utrip1.save()
        response = self.client.post(
            reverse("matching:react_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "sender_utrip_id": self.utrip2.id,
                "sender_id": self.user2.id,
                "pending_request": "Matched",
            },
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "Cannot accept/reject you with other user, as your current trip is inactive.",
        )
        self.utrip1.is_active = True
        self.utrip1.save()

        self.utrip2.is_active = False
        self.utrip2.save()
        response = self.client.post(
            reverse("matching:react_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "sender_utrip_id": self.utrip2.id,
                "sender_id": self.user2.id,
                "pending_request": "Matched",
            },
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "The sender trip or the sender itself is not active anymore, "
            "cannot accept/reject the request.",
        )

    def test_show_matches(self):
        pass

    def test_unmatch(self):
        self.client.login(username="matching_user2", password=self.password)
        _ = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip2.id}),
            {
                "receiver_utrip_id": self.utrip1.id,
                "receiver_uid": self.user1.id,
            },
            follow=True,
        )
        self.client.logout()
        self.client.login(username="matching_user", password=self.password)
        self.utrip1.is_active = True
        self.utrip1.save()
        response = self.client.post(
            reverse("matching:react_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "sender_utrip_id": self.utrip2.id,
                "sender_id": self.user2.id,
                "pending_request": "Matched",
            },
            follow=True,
        )
        response = self.client.post(
            reverse("matching:unmatch", kwargs={"utrip_id": self.utrip1.id}),
            {"other_uid": self.user1.id},
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "No match found, other user might have already unmatched",
        )
        response = self.client.post(
            reverse("matching:unmatch", kwargs={"utrip_id": 0}),
            {"other_uid": self.user1.id},
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "Please select a valid trip",
        )

    def test_save_matches(self):
        self.client.login(username="matching_user2", password=self.password)
        _ = self.client.post(
            reverse("matching:send_request", kwargs={"utrip_id": self.utrip2.id}),
            {
                "receiver_utrip_id": self.utrip1.id,
                "receiver_uid": self.user1.id,
            },
            follow=True,
        )
        self.client.logout()
        self.client.login(username="matching_user", password=self.password)
        self.utrip1.is_active = True
        self.utrip1.save()
        response = self.client.post(
            reverse("matching:react_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "sender_utrip_id": self.utrip2.id,
                "sender_id": self.user2.id,
                "pending_request": "Matched",
            },
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "You are successfully matched with the sender",
        )
        t = Thread.objects.filter(Q(first_user=self.user1) & Q(second_user=self.user2))
        u = Thread.objects.filter(Q(first_user=self.user2) & Q(second_user=self.user1))
        self.assertQuerysetEqual(t, Thread.objects.none())
        self.assertTrue(u[0].first_user, self.user2)
        response = self.client.post(
            reverse("matching:react_request", kwargs={"utrip_id": self.utrip1.id}),
            {
                "sender_utrip_id": self.utrip2.id,
                "sender_id": self.user2.id,
                "pending_request": "Matched",
            },
            follow=True,
        )
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            "This matching request has already been accepted",
        )
        response = self.client.post(
            reverse("matching:unmatch", kwargs={"utrip_id": self.utrip1.id}),
            {"other_uid": self.user2.id},
            follow=True,
        )
        u = Thread.objects.filter(Q(first_user=self.user2) & Q(second_user=self.user1))
        self.assertQuerysetEqual(u, Thread.objects.none())
        self.assertEqual(response.status_code, 200)
