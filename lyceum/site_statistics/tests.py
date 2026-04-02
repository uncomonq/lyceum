__all__ = ()
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import override_settings, TestCase
from django.urls import reverse

User = get_user_model()


@override_settings(ALLOW_REVERSE=False)
class SiteStatisticsViewsTests(TestCase):
    fixtures = ["fixtures/test_site_statistics.json"]

    def test_users_statistics_renders_best_and_worst_items(self):
        response = self.client.get(reverse("statistics:users"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "stat_user_1")
        self.assertContains(response, "Товар А")
        self.assertContains(response, "Товар Б")
        self.assertContains(response, "3,00")

    def test_items_statistics_renders_latest_min_and_max_rating(self):
        response = self.client.get(reverse("statistics:items"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Товар А")
        self.assertContains(response, "stat_user_1 (5)")
        self.assertContains(response, "stat_user_2 (3)")
        self.assertContains(response, "Товар Б")
        self.assertContains(response, "stat_user_1 (1)")

    def test_my_items_requires_authentication(self):
        response = self.client.get(reverse("statistics:my_items"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(reverse("users:login"), response.url)

    def test_my_items_shows_current_user_ratings(self):
        self.client.force_login(User.objects.get(username="stat_user_1"))

        response = self.client.get(reverse("statistics:my_items"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Товар А")
        self.assertContains(response, "Товар Б")
        self.assertContains(response, "5")
        self.assertContains(response, "1")
