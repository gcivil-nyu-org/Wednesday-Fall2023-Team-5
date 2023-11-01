# Create your tests here.
from django.test import SimpleTestCase


from django.urls import reverse
from django.test import Client


class TestsHomeDefaultView(SimpleTestCase):
    client = Client()

    def test_home_page(self):
        response = self.client.get(reverse("home_default:home_page"))
        self.assertEqual(response.status_code, 200)
