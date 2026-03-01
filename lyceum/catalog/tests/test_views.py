from http import HTTPStatus

from django.test import override_settings, TestCase
from django.urls import reverse
from parameterized import parameterized


@override_settings(ALLOW_REVERSE=False)
class CatalogViewsTests(TestCase):
    def test_item_list_returns_ok(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_item_list_uses_expected_template(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertTemplateUsed(response, "catalog/item_list.html")

    def test_item_list_contains_all_static_items(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)
        self.assertEqual(len(response.context["items"]), 4)

    @parameterized.expand(
        [
            ("existing_pk", 2, "Чай улун"),
            ("fallback_pk", 999, "Кофе в зёрнах"),
        ],
    )
    def test_item_detail_returns_expected_item(self, _, pk, expected_name):
        response = self.client.get(reverse("catalog:item_detail", args=[pk]))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "catalog/item.html")
        self.assertIn("item", response.context)
        self.assertEqual(response.context["item"]["name"], expected_name)
        self.assertEqual(response.context["item"]["pk"], pk)
