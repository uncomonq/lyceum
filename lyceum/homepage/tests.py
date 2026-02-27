from http import HTTPStatus

from django.test import TestCase

__all__ = ("HomepageURLTests", "CoffeeEndpointTests")


class HomepageURLTests(TestCase):
    def test_homepage_url_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CoffeeEndpointTests(TestCase):
    def test_coffee_status(self):
        response = self.client.get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_content(self):
        resopnse = self.client.get("/coffee/")
        self.assertEqual(resopnse.content, "Я чайник".encode())
