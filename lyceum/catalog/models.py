__all__ = (
    "Tag",
    "Category",
    "ItemQuerySet",
    "ItemManager",
    "Item",
    "MainImage",
    "ItemImage",
)
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
import django.db.models
import django.utils.safestring
import sorl.thumbnail
import tinymce.models

import catalog.utils
import catalog.validators
import core.models


class Tag(core.models.CommonModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="Должен содержать только латинские буквы, цифры,"
        " дефисы и знаки подчёркивания",
    )
    normalized_name = django.db.models.CharField(
        "normalized_name",
        max_length=200,
        null=False,
        blank=False,
        editable=False,
        unique=False,
        error_messages={"unique": "Объект с похожим именем уже существует."},
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def save(self, *args, **kwargs):
        self.normalized_name = catalog.utils.normalize_name(self.name or "")
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        norm = catalog.utils.normalize_name(self.name)
        self.normalized_name = norm

        qs = self.__class__.objects.filter(normalized_name=norm)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                {"name": "Категория с похожим именем уже существует."},
            )


class Category(core.models.CommonModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="Должен содержать только латинские буквы, цифры,"
        " дефисы и знаки подчёркивания",
    )
    weight = django.db.models.PositiveSmallIntegerField(
        "вес",
        default=100,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ],
        help_text="От 1 до 32767",
    )
    normalized_name = django.db.models.CharField(
        "normalized_name",
        max_length=200,
        null=False,
        blank=False,
        editable=False,
        unique=False,
        error_messages={"unique": "Объект с похожим именем уже существует."},
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["weight"]

    def save(self, *args, **kwargs):
        self.normalized_name = catalog.utils.normalize_name(self.name or "")
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        norm = catalog.utils.normalize_name(self.name)
        self.normalized_name = norm

        qs = self.__class__.objects.filter(normalized_name=norm)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                {"name": "Категория с похожим именем уже существует."},
            )


class ItemQuerySet(django.db.models.QuerySet):
    def _for_card(self):
        return (
            self.select_related("category")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name",
                    ),
                ),
            )
            .only("name", "text", "category__name")
        )

    def published(self):
        return (
            self.filter(is_published=True, category__is_published=True)
            ._for_card()
            .order_by("category__name", "name")
        )

    def on_main(self):
        return self.published().filter(is_on_main=True).order_by("name")

    def new_items(self, from_datetime):
        return (
            self.filter(created_at__gte=from_datetime)
            ._for_card()
            .order_by("?")[:5]
        )

    def friday_items(self):
        return (
            self.filter(updated_at__week_day=6)
            ._for_card()
            .order_by(
                "-updated_at",
            )[:5]
        )

    def unverified_items(self):
        return self.filter(
            updated_at=django.db.models.F("created_at"),
        )._for_card()


class ItemManager(django.db.models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def on_main(self):
        return self.get_queryset().on_main()

    def new_items(self, from_datetime):
        return self.get_queryset().new_items(from_datetime)

    def friday_items(self):
        return self.get_queryset().friday_items()

    def unverified_items(self):
        return self.get_queryset().unverified_items()


class Item(core.models.CommonModel):
    objects = ItemManager()
    created_at = django.db.models.DateTimeField(
        "дата создания",
        auto_now_add=True,
        null=True,
        blank=True,
    )
    updated_at = django.db.models.DateTimeField(
        "дата изменения",
        auto_now=True,
        null=True,
        blank=True,
    )
    text = tinymce.models.HTMLField(
        "текст",
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
        ],
        help_text="Должно содержать слова «превосходно» или «роскошно»",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        related_query_name="item",
        verbose_name="категория",
    )

    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="items",
        related_query_name="item",
        blank=True,
        verbose_name="теги",
    )

    is_on_main = django.db.models.BooleanField(
        default=False,
        verbose_name="на главной",
        help_text="Статус отображения на главной.",
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def main_image_preview(self):
        if not hasattr(self, "main_image"):
            return ""
        thumb = sorl.thumbnail.get_thumbnail(
            self.main_image.image,
            "300x300",
            crop="center",
            quality=70,
        )

        return django.utils.safestring.mark_safe(
            f'<img src="{thumb.url}" width="50" height="50" '
            f'style="object-fit:cover;" />',
        )


class MainImage(django.db.models.Model):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        related_query_name="main_image",
        verbose_name="товар",
    )

    image = django.db.models.ImageField(
        upload_to="items/main/",
        verbose_name="главное изображение",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"

    def __str__(self):
        return f"Главное изображение: {self.item.name}"


class ItemImage(django.db.models.Model):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        related_query_name="image",
        verbose_name="товар",
    )
    image = django.db.models.ImageField(
        upload_to="items/gallery/",
        verbose_name="изображение",
    )
    ordering = django.db.models.PositiveIntegerField(
        "порядок",
        default=0,
    )

    class Meta:
        ordering = ["ordering"]
        verbose_name = "изображение товара"
        verbose_name_plural = "изображения товара"

    def __str__(self):
        return f"{self.item.name} — image #{self.pk}"
