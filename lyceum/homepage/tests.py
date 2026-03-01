__all__ = (
    "HomepageURLTests",
    "CoffeeEndpointTests",
    "NavigationLabelsTests",
)
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import override


class HomepageURLTests(TestCase):
    def test_homepage_url_exists(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class CoffeeEndpointTests(TestCase):
    def test_coffee_status(self):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_content(self):
        response = self.client.get(reverse("homepage:coffee"))
        self.assertEqual(response.content, "Я чайник".encode())


class NavigationLabelsTests(TestCase):
    def test_home_page_labels(self):
        response = self.client.get(reverse("homepage:main"))

        self.assertContains(response, "Главная")
        self.assertContains(response, "О проекте")
        self.assertContains(response, "Список товаров")
        self.assertNotContains(response, "На главную")

    def test_catalog_page_labels(self):
        response = self.client.get(reverse("catalog:item_list"))

        self.assertContains(response, "На главную")
        self.assertContains(response, "О проекте")
        self.assertContains(response, "Список товаров")
        self.assertNotContains(response, "К списку товаров")

    def test_catalog_page_labels_in_english(self):
        with override("en"):
            response = self.client.get(reverse("catalog:item_list"))

        self.assertContains(response, "To home")
        self.assertContains(response, "About")
        self.assertContains(response, "Items")
        self.assertNotContains(response, "К списку товаров")

    def test_home_page_labels_in_english(self):
        with override("en"):
            response = self.client.get(reverse("homepage:main"))

        self.assertContains(response, "Home")
        self.assertContains(response, "About")
        self.assertContains(response, "Items")
        self.assertNotContains(response, "На главную")
