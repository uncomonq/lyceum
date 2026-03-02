__all__ = (
    "HomepageURLTests",
    "CoffeeEndpointTests",
)
from http import HTTPStatus

from django.test import override_settings, TestCase
from django.urls import reverse
from parameterized import parameterized

from catalog.models import Category, Item, Tag


@override_settings(ALLOW_REVERSE=False)
class HomepageURLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Напитки",
            slug="drinks",
            weight=5,
            normalized_name="напитки",
        )
        cls.tag = Tag.objects.create(
            name="Популярное",
            slug="popular",
            normalized_name="популярное",
        )

        cls.item_on_main_a = Item.objects.create(
            name="Американо",
            text="<p>Роскошно бодрящий кофе для утра.</p>",
            category=cls.category,
            is_published=True,
            is_on_main=True,
        )
        cls.item_on_main_a.tags.add(cls.tag)

        cls.item_on_main_b = Item.objects.create(
            name="Латте",
            text="<p>Превосходно нежный молочный кофе.</p>",
            category=cls.category,
            is_published=True,
            is_on_main=True,
        )

        cls.item_not_on_main = Item.objects.create(
            name="Эспрессо",
            text="<p>Роскошно насыщенный шот кофе.</p>",
            category=cls.category,
            is_published=True,
            is_on_main=False,
        )

        cls.item_unpublished = Item.objects.create(
            name="Мокка",
            text="<p>Превосходно шоколадный вкус.</p>",
            category=cls.category,
            is_published=False,
            is_on_main=True,
        )

    def test_homepage_url_exists(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_uses_expected_template(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertTemplateUsed(response, "homepage/main.html")

    def test_homepage_context_contains_published_items_on_main(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertIn("items", response.context)

        items = list(response.context["items"])

        self.assertEqual(items, [self.item_on_main_a, self.item_on_main_b])
        self.assertNotIn(self.item_not_on_main, items)
        self.assertNotIn(self.item_unpublished, items)

    def test_homepage_context_items_ordered_by_name(self):
        response = self.client.get(reverse("homepage:main"))
        items = list(response.context["items"])

        self.assertEqual([item.name for item in items], ["Американо", "Латте"])


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
