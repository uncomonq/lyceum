__all__ = ()
from datetime import timedelta
from http import HTTPStatus

from django.test import override_settings, TestCase
from django.urls import reverse
import django.utils.timezone


from catalog.models import Category, Item, ItemImage, MainImage, Tag


@override_settings(ALLOW_REVERSE=False)
class CatalogViewsTests(TestCase):
    fixtures = ["fixtures/test_catalog_views.json"]

    @classmethod
    def setUpTestData(cls):
        cls.category_a = Category.objects.get(pk=101)
        cls.category_b = Category.objects.get(pk=102)
        cls.tag_hot = Tag.objects.get(pk=101)
        cls.tag_new = Tag.objects.get(pk=102)

        cls.item_published_a = Item.objects.get(pk=101)
        cls.item_published_b = Item.objects.get(pk=102)
        cls.item_unpublished = Item.objects.get(pk=103)
        cls.category_empty = Category.objects.get(pk=103)
        cls.main_image = MainImage.objects.get(pk=101)
        cls.extra_image = ItemImage.objects.get(pk=101)

        cls.item_published_a.tags.add(cls.tag_new)
        cls.item_published_b.tags.add(cls.tag_hot, cls.tag_new)
        now = django.utils.timezone.now()
        Item.objects.filter(pk=cls.item_published_a.pk).update(
            created_at=now - timedelta(days=1),
            updated_at=now - timedelta(days=1),
        )
        Item.objects.filter(pk=cls.item_published_b.pk).update(
            created_at=now - timedelta(days=2),
            updated_at=now - timedelta(days=2),
        )
        cls.old_item = Item.objects.create(
            name="Старый товар",
            text="<p>Роскошно старый товар.</p>",
            category=cls.category_a,
            is_published=False,
        )
        Item.objects.filter(pk=cls.old_item.pk).update(
            created_at=now - timedelta(days=20),
            updated_at=now - timedelta(days=20),
        )

        cls.friday_items = []
        friday_date = now - timedelta(days=(now.weekday() - 4) % 7)
        for index in range(6):
            item = Item.objects.create(
                name=f"Пятничный {index}",
                text="<p>Превосходно пятничный товар.</p>",
                category=cls.category_b,
                is_published=False,
            )
            ts = friday_date - timedelta(weeks=index)
            Item.objects.filter(pk=item.pk).update(
                created_at=ts - timedelta(days=1),
                updated_at=ts,
            )
            cls.friday_items.append(item)

    def test_item_list_returns_ok(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_item_list_uses_expected_template(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertTemplateUsed(response, "catalog/item_list.html")

    def test_item_list_context_contains_items_key(self):
        response = self.client.get(reverse("catalog:item_list"))

        self.assertIn("items", response.context)

    def test_item_list_context_contains_expected_count(self):
        response = self.client.get(reverse("catalog:item_list"))

        self.assertEqual(len(response.context["items"]), 2)

    def test_item_list_context_contains_only_published_items(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = list(response.context["items"])

        self.assertEqual(items, [self.item_published_a, self.item_published_b])

    def test_item_list_context_excludes_unpublished_items(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = list(response.context["items"])

        self.assertNotIn(self.item_unpublished, items)

    def test_item_list_context_is_ordered_by_category_name(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = list(response.context["items"])

        self.assertEqual(items[0].category.name, "Аксессуары")
        self.assertEqual(items[1].category.name, "Электроника")

    def test_item_list_groups_items_by_category_in_page(self):
        response = self.client.get(reverse("catalog:item_list"))

        content = response.content.decode("utf-8")

        self.assertIn("Аксессуары", content)
        self.assertIn("Электроника", content)
        self.assertIn("Ремешок", content)
        self.assertIn("Планшет", content)

    def test_item_list_does_not_show_categories_without_active_items(self):
        response = self.client.get(reverse("catalog:item_list"))

        self.assertNotIn("Пустая", response.content.decode("utf-8"))

    def test_published_manager_defers_filtered_fields(self):
        item = Item.objects.published().first()

        self.assertIn("is_published", item.get_deferred_fields())
        self.assertIn("is_on_main", item.get_deferred_fields())

    def test_published_manager_prefetches_tags(self):
        item = list(Item.objects.published())[0]

        self.assertIn("tags", item._prefetched_objects_cache)

    def test_item_new_uses_shared_template(self):
        response = self.client.get(reverse("catalog:item_new"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "catalog/item_list.html")

    def test_item_new_contains_only_last_week_and_limit_five(self):
        response = self.client.get(reverse("catalog:item_new"))

        items = list(response.context["items"])
        threshold = django.utils.timezone.now() - timedelta(days=7)

        self.assertLessEqual(len(items), 5)
        for item in items:
            self.assertGreaterEqual(item.created_at, threshold)

    def test_item_friday_returns_five_items(self):
        response = self.client.get(reverse("catalog:item_friday"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "catalog/item_list.html")
        self.assertEqual(len(response.context["items"]), 5)

    def test_item_unverified_returns_items_without_updates(self):
        response = self.client.get(reverse("catalog:item_unverified"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "catalog/item_list.html")
        for item in response.context["items"]:
            self.assertEqual(item.created_at, item.updated_at)

    def test_item_detail_returns_ok(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[self.item_published_b.pk]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_item_detail_uses_expected_template(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[self.item_published_b.pk]),
        )

        self.assertTemplateUsed(response, "catalog/item.html")

    def test_item_detail_contains_expected_context_keys(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[self.item_published_b.pk]),
        )

        self.assertIn("item", response.context)
        self.assertIn("main_image", response.context)

    def test_item_detail_context_contains_expected_item(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[self.item_published_b.pk]),
        )

        self.assertEqual(response.context["item"].pk, self.item_published_b.pk)

    def test_item_detail_context_contains_expected_category(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[self.item_published_b.pk]),
        )

        self.assertEqual(response.context["item"].category.name, "Электроника")

    def test_item_detail_context_contains_expected_tags(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[self.item_published_b.pk]),
        )

        item = response.context["item"]

        self.assertEqual(
            {tag.name for tag in item.tags.all()},
            {"Хит", "Новинка"},
        )

    def test_item_detail_context_contains_expected_main_image(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[self.item_published_b.pk]),
        )

        self.assertEqual(response.context["main_image"], self.main_image)

    def test_item_detail_context_contains_expected_extra_images(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[self.item_published_b.pk]),
        )

        item = response.context["item"]

        self.assertEqual(list(item.images.all()), [self.extra_image])

    def test_download_main_image_returns_attachment(self):
        response = self.client.get(
            reverse("download_media", args=[self.main_image.image.name]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("main", response["Content-Disposition"])
        self.assertIn(".jpg", response["Content-Disposition"])

    def test_download_additional_image_returns_attachment(self):
        response = self.client.get(
            reverse("download_media", args=[self.extra_image.image.name]),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("extra", response["Content-Disposition"])
        self.assertIn(".jpg", response["Content-Disposition"])

    def test_download_unknown_file_returns_404(self):
        response = self.client.get(
            reverse("download_media", args=["items/main/not-found.jpg"]),
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_item_detail_returns_404_for_unknown_pk(self):
        response = self.client.get(
            reverse("catalog:item_detail", args=[999999]),
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
