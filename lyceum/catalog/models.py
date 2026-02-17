from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    validate_slug,
)
import django.db.models

from catalog.validators import ValidateMustContain
from core.models import CommonModel


class CatalogTag(CommonModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        validators=[validate_slug],
        help_text="Должен содержать только латинские буквы, цифры,"
        " дефисы и знаки подчёркивания",
    )
    normalized_name = django.db.models.CharField(
        "нормализованное имя",
        max_length=200,
        null=True,
        blank=True,
        editable=False,
        unique=False,
        help_text="Нормализованное имя для уникальности "
        "(генерируется автоматически).",
    )

    def clean(self):
        super().clean()

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class CatalogCategory(CommonModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        validators=[validate_slug],
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
        "нормализованное имя",
        max_length=200,
        null=True,
        blank=True,
        editable=False,
        unique=False,
        help_text="Нормализованное имя для уникальности "
        "(генерируется автоматически).",
    )

    def clean(self):
        super().clean()

    class Meta:
        db_table = "catalog_category"
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["weight"]

    def __str__(self):
        return self.name[:15]


class CatalogItem(CommonModel):
    text = django.db.models.TextField(
        "текст",
        validators=[ValidateMustContain("превосходно", "роскошно")],
        help_text="Должно содержать слова «превосходно» или «роскошно»",
    )
    category = django.db.models.ForeignKey(
        CatalogCategory,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        verbose_name="категория",
    )

    tags = django.db.models.ManyToManyField(
        CatalogTag,
        related_name="items",
        blank=True,
        verbose_name="теги",
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]


Category = CatalogCategory
Tag = CatalogTag
Item = CatalogItem
