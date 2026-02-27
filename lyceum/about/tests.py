from http import HTTPStatus

from django.test import TestCase

__all__ = ("AboutURLTests",)


class AboutURLTests(TestCase):
    def test_about_url_exists(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
