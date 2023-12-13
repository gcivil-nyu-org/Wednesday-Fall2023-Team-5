from django.db.models import Q
from django.test import TestCase, Client  # noqa


# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse

from chat.models import Thread, ChatMessage
from user_profile.models import UserImages

from datetime import datetime


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "thread_password"
        self.user1 = User.objects.create_user(
            username="thread_user3",
            email="thread_user3@nyu.edu",
            password=self.password,
        )
        self.user2 = User.objects.create_user(
            username="thread_user4",
            email="thread_user4@nyu.edu",
            password=self.password,
        )
        self.user3 = User.objects.create_user(
            username="no_thread_user5",
            email="thread_user5@nyu.edu",
            password=self.password,
        )
        self.user1.userprofile.dob = datetime(2000, 9, 22)
        self.user2.userprofile.dob = datetime(2000, 9, 22)
        self.user1.userprofile.images = UserImages.objects.create(
            user_profile=self.user1.userprofile,
            image="profileImages/great-gatsby-background-1.jpg",
        )
        self.user2.userprofile.images = UserImages.objects.create(
            user_profile=self.user2.userprofile,
            image="profileImages/great-gatsby-background-1.jpg",
        )
        self.user1.save()
        self.user2.save()

    def test_threads_view(self):
        Thread.objects.create(
            first_user=self.user1, second_user=self.user2, updated=datetime.utcnow()
        )
        t = Thread.objects.filter(Q(first_user=self.user1) & Q(second_user=self.user2))
        user1_login = self.client.login(username="thread_user3", password=self.password)
        self.assertTrue(user1_login)
        response = self.client.get(reverse("chat:threads_page"))
        self.assertEqual(response.status_code, 302)
        print(t[0].first_user.id)
        print(t[0].second_user.id)
        print(t[0].id)
        url = "/chat/thread" + "/" + str(t[0].id) + "/" + str(t[0].second_user.id)
        self.assertRedirects(response, url)

    def test_no_threads_view(self):
        user4_login = self.client.login(
            username="no_thread_user5", password=self.password
        )
        self.assertTrue(user4_login)
        response = self.client.get(reverse("chat:threads_page"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/chat/thread/")

    class TestModelSave(TestCase):
        def setUp(self):
            self.password = "thread_password"
            self.user1 = User.objects.create_user(
                username="thread_user",
                email="thread_user@nyu.edu",
                password=self.password,
            )
            self.user2 = User.objects.create_user(
                username="thread_user2",
                email="thread_user2@nyu.edu",
                password=self.password,
            )
            self.user1.userprofile.dob = datetime(2000, 9, 22)
            self.user2.userprofile.dob = datetime(2000, 9, 22)
            self.user1.userprofile.images = UserImages.objects.create(
                user_profile=self.user1.userprofile,
                image="profileImages/great-gatsby-background-1.jpg",
            )
            self.user1.save()
            self.user2.save()

        def test_save(self):
            Thread.objects.create(
                first_user=self.user1, second_user=self.user2, updated=datetime.utcnow()
            )
            t = Thread.objects.filter(
                Q(first_user=self.user1) & Q(second_user=self.user2)
            )
            ChatMessage.objects.create(
                thread=t, sending_user=self.user1, message="hello"
            )
            self.assertEqual(
                t[0].first_user_image_url,
                "/media/profileImages/great-gatsby-background-1.jpg",
            )
            self.assertEqual(
                t[0].second_user_image_url,
                "/media/profileImages/great-gatsby-background-1.jpg",
            )
