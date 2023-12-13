from django.db.models import Q
from django.test import TestCase  # noqa


# Create your tests here.
from django.contrib.auth.models import User


from chat.models import Thread
from user_profile.models import UserImages

from datetime import datetime


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
        t = Thread.objects.filter(Q(first_user=self.user1) & Q(second_user=self.user2))
        self.assertEqual(
            t[0].first_user_image_url,
            "/media/profileImages/great-gatsby-background-1.jpg",
        )
        self.assertEqual(t[0].second_user_image_url, "/media/default_avatar.png")
