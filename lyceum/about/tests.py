__all__ = ()
from http import HTTPStatus

from django.test import override_settings, TestCase
from django.urls import reverse


@override_settings(ALLOW_REVERSE=False)
class AboutURLTests(TestCase):
    def test_about_page_available_and_uses_template(self):
        response = self.client.get(reverse("about:about"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "about/about.html")
