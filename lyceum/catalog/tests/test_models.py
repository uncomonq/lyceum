__all__ = ()
from unittest import mock

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from parameterized import parameterized

from catalog.models import Category, Item, ItemImage, MainImage, Tag
from catalog.utils import normalize_name
from catalog.validators import ValidateMustContain


class ItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Тестовая категория",
            slug="test-category",
            is_published=True,
            weight=100,
        )

    def test_create_item_positive(self):
        item = Item(
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

    def test_validate_keywords_with_html_tags(self):
        self.validator("<p><strong>Превосходно</strong> выглядит</p>")

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
            "  ПреВосХодно!  ": "prevoskhodno",
            "роскошно!!!": "roskoshno",
            "нов-инка": "novinka",
            "pockoшno": "pockoshno",
            "aA": "aa",
        }
        for inp, want in cases.items():
            self.assertEqual(normalize_name(inp), want)


class CategoryNormalizeUniqueTests(TestCase):
    def setUp(self):
        Category.objects.create(
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
        c = Category(name=name, slug="x", is_published=True, weight=1)
        with self.assertRaises(ValidationError):
            c.full_clean()


class CategoryWeightValidationTests(TestCase):
    @parameterized.expand(
        [
            ("min_boundary", 1),
            ("max_boundary", 32767),
        ],
    )
    def test_weight_boundaries_are_valid(self, _, weight):
        category = Category(
            name=f"Категория {weight}",
            slug=f"cat-{weight}",
            is_published=True,
            weight=weight,
        )
        category.full_clean()

    @parameterized.expand(
        [
            ("below_min", 0),
            ("above_max", 32768),
        ],
    )
    def test_weight_outside_boundaries_is_invalid(self, _, weight):
        category = Category(
            name=f"Категория {weight}",
            slug=f"cat-invalid-{weight}",
            is_published=True,
            weight=weight,
        )
        with self.assertRaises(ValidationError):
            category.full_clean()


class TagNormalizeUniqueTests(TestCase):
    def setUp(self):
        Tag.objects.create(name="Новая", slug="new-tag", is_published=True)

    @parameterized.expand(
        [
            ("same_case", "Новая"),
            ("spaces", " новая "),
            ("mixed_case", "нОвая!"),
            ("latin_char", "Nовая"),
        ],
    )
    def test_tag_canonical_conflicts(self, _, name):
        tag = Tag(
            name=name,
            slug=f"tag-{normalize_name(name)}",
            is_published=True,
        )
        with self.assertRaises(ValidationError):
            tag.full_clean()


class ItemImageOrderingTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Категория для изображений",
            slug="cat-images",
            is_published=True,
            weight=100,
        )
        self.item = Item.objects.create(
            name="Товар с изображениями",
            text="Превосходно работает в тестах.",
            category=self.category,
            is_published=True,
        )

    def test_images_are_sorted_by_ordering(self):
        ItemImage.objects.create(
            item=self.item,
            image=SimpleUploadedFile(
                "image-20.jpg",
                b"filecontent-20",
                content_type="image/jpeg",
            ),
            ordering=20,
        )
        ItemImage.objects.create(
            item=self.item,
            image=SimpleUploadedFile(
                "image-5.jpg",
                b"filecontent-5",
                content_type="image/jpeg",
            ),
            ordering=5,
        )
        ItemImage.objects.create(
            item=self.item,
            image=SimpleUploadedFile(
                "image-10.jpg",
                b"filecontent-10",
                content_type="image/jpeg",
            ),
            ordering=10,
        )

        orderings = list(self.item.images.values_list("ordering", flat=True))
        self.assertEqual(orderings, [5, 10, 20])


class ImageStringRepresentationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Категория str",
            slug="cat-str",
            is_published=True,
            weight=100,
        )
        self.item = Item.objects.create(
            name="Товар str",
            text="Роскошно проходит тесты.",
            category=self.category,
            is_published=True,
        )

    def test_main_image_str(self):
        main_image = MainImage.objects.create(
            item=self.item,
            image=SimpleUploadedFile(
                "main.jpg",
                b"main-file",
                content_type="image/jpeg",
            ),
        )
        self.assertEqual(
            str(main_image),
            f"Главное изображение: {self.item.name}",
        )

    def test_item_image_str(self):
        item_image = ItemImage.objects.create(
            item=self.item,
            image=SimpleUploadedFile(
                "gallery.jpg",
                b"gallery-file",
                content_type="image/jpeg",
            ),
            ordering=1,
        )
        self.assertEqual(
            str(item_image),
            f"{self.item.name} — image #{item_image.pk}",
        )


class ItemMainImagePreviewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Категория preview",
            slug="cat-preview",
            is_published=True,
            weight=100,
        )
        self.item = Item.objects.create(
            name="Товар preview",
            text="Роскошно смотрится в каталоге.",
            category=self.category,
            is_published=True,
        )

    def test_main_image_preview_without_image_returns_empty_string(self):
        self.assertEqual(self.item.main_image_preview(), "")

    @mock.patch("catalog.models.sorl.thumbnail.get_thumbnail")
    def test_main_image_preview_returns_img_markup(self, thumbnail_mock):
        thumbnail_mock.return_value.url = "/media/thumb.jpg"

        MainImage.objects.create(
            item=self.item,
            image=SimpleUploadedFile(
                "preview.jpg",
                b"preview-file",
                content_type="image/jpeg",
            ),
        )

        preview_html = self.item.main_image_preview()

        self.assertIn('<img src="/media/thumb.jpg"', preview_html)
        self.assertIn('width="50" height="50"', preview_html)
        thumbnail_mock.assert_called_once()
