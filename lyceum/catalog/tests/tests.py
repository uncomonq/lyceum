from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

import catalog.models

__all__ = ("ItemDetailViewTests",)


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
        self.assertEqual(response.status_code, HTTPStatus.OK)
