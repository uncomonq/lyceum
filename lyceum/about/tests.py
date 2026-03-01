__all__ = ("AboutURLTests",)
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class AboutURLTests(TestCase):
    def test_about_url_exists(self):
        response = self.client.get(reverse("about:about"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
