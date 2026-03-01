__all__ = (
    "HomepageURLTests",
    "CoffeeEndpointTests",
)
from http import HTTPStatus

from django.test import override_settings, TestCase
from django.urls import reverse
from parameterized import parameterized


@override_settings(ALLOW_REVERSE=False)
class HomepageURLTests(TestCase):
    def test_homepage_url_exists(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_uses_expected_template(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertTemplateUsed(response, "homepage/main.html")

    def test_homepage_contains_three_items(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertIn("items", response.context)
        self.assertEqual(len(response.context["items"]), 3)


@override_settings(ALLOW_REVERSE=False)
class CoffeeEndpointTests(TestCase):
    def test_coffee_status(self):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_content(self):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response.content, "Я чайник".encode())

    @parameterized.expand(
        [
            ("response_is_text", "text/html; charset=utf-8"),
        ],
    )
    def test_coffee_content_type(self, _, expected):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response["Content-Type"], expected)
