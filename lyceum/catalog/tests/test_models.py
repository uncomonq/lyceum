from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from catalog.models import CatalogCategory, CatalogItem
from catalog.utils import normalize_name
from catalog.validators import ValidateMustContain


class CatalogItemModelTest(TestCase):
    def setUp(self):
        self.category = CatalogCategory.objects.create(
            name="Тестовая категория",
            slug="test-category",
            is_published=True,
            weight=100,
        )

    def test_create_item_positive(self):
        item = CatalogItem(
            name="Тестовый товар",
            text="Корректный текст, превосходно работает.",
            category=self.category,
            is_published=True,
        )

        item.full_clean()
        item.save()

        self.assertEqual(item.name, "Тестовый товар")


class ValidateKeywordsTest(TestCase):

    def setUp(self):
        self.validator = ValidateMustContain(
            "превосходно",
            "роскошно",
        )

    @parameterized.expand(
        [
            ("good_text_1", "Роскошно выглядит"),
            ("good_text_2", "Превосходно выполняет свою работу"),
            ("good_text_3", "Он просто роскошно — превосходен"),
        ],
    )
    def test_validate_keywords_positive(self, name, text):
        self.validator(text)

    @parameterized.expand(
        [
            ("bad_text_1", "Купить бесплатно"),
            ("bad_text_2", "роскошнопривет"),
            ("bad_text_3", "лучшийпревосходно"),
            ("bad_text_4", "роскшонопревосходный"),
        ],
    )
    def test_validate_keywords_negative(self, name, text):
        with self.assertRaises(ValidationError):
            self.validator(text)


class NormalizeTests(TestCase):
    def test_normalize_basic(self):
        cases = {
            "  ПреВосХодно!  ": "превосходно",
            "роскошно!!!": "роскошно",
            "RosKошно": "роскошно",  # лат/кир mix
            "нов-инка": "новинка",
            "aA": "аа",  # лат a -> кир а
        }
        for inp, want in cases.items():
            self.assertEqual(normalize_name(inp), want)


class CategoryNormalizeUniqueTests(TestCase):
    def setUp(self):
        CatalogCategory.objects.create(
            name="Новая",
            slug="one",
            is_published=True,
            weight=10,
        )

    @parameterized.expand(
        [
            ("Новая",),
            (" новая ",),
            ("нОвая!",),
            ("Nовая",),
        ],
    )
    def test_canonical_conflicts(self, name):
        c = CatalogCategory(name=name, slug="x", is_published=True, weight=1)
        with self.assertRaises(ValidationError):
            c.full_clean()
