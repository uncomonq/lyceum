from http import HTTPStatus
from urllib.parse import quote

from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

import catalog.models

__all__ = ("CatalogViewsTests",)


class ItemDetailViewTests(TestCase):
    def setUp(self):
        self.category = catalog.models.Category.objects.create(
            name="Тестовая категория",
            slug="test-category",
            is_published=True,
            weight=1,
        )
        self.item = catalog.models.Item.objects.create(
            name="Тестовый товар",
            text="Превосходно",
            category=self.category,
            is_published=True,
        )

    def test_item_detail_view(self):
        url = reverse("catalog:item_detail", args=[self.item.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CatalogViewsTests(TestCase):
    VALID_INPUTS = [
        "1",
        "01",
        "001",
        "010",
        "10",
        "100",
        "42",
        "123",
    ]

    INVALID_INPUTS = [
        "0",
        "-0",
        "-1",
        "-42",
        "1.0",
        "1.5",
        "0.1",
        "",
        "00",
        "1a",
        "a1",
        "1a2",
        "a12",
        "12a",
        "a1b2",
        "$",
        "%",
        "^",
        "@",
        "1$",
        "$1",
        "1%2",
        "abc",
    ]

    @parameterized.expand(VALID_INPUTS)
    def test_re_positive_numbers(self, num):
        url = reverse("catalog:re", args=[num])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode(), str(int(num)))

    @parameterized.expand(INVALID_INPUTS)
    def test_re_invalid_numbers(self, inval):
        seg = quote(inval, safe="")

        url_re = reverse("catalog:re", args=[seg])
        resp_re = self.client.get(url_re)
        self.assertEqual(resp_re.status_code, HTTPStatus.NOT_FOUND)

        url_conv = reverse("catalog:converter", args=[seg])
        resp_conv = self.client.get(url_conv)
        self.assertEqual(resp_conv.status_code, HTTPStatus.NOT_FOUND)
