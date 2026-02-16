from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    validate_slug,
)
import django.db.models

from core.models import CommonModel
from .validators import validate_keywords


class CatalogTag(CommonModel):
    slug = django.db.models.SlugField(
        "Слаг",
        max_length=200,
        unique=True,
        validators=[validate_slug],
        help_text="Должен содержать только латинские буквы, цифры,"
        " дефисы и знаки подчёркивания",
    )

    class Meta:
        db_table = "catalog_tag"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class CatalogCategory(CommonModel):
    slug = django.db.models.SlugField(
        "Слаг",
        max_length=200,
        unique=True,
        validators=[validate_slug],
        help_text="Должен содержать только латинские буквы, цифры,"
        " дефисы и знаки подчёркивания",
    )
    weight = django.db.models.PositiveSmallIntegerField(
        "Вес",
        default=100,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ],
        help_text="От 1 до 32767",
    )

    class Meta:
        db_table = "catalog_category"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["weight"]

    def __str__(self):
        return self.name


class CatalogItem(CommonModel):
    text = django.db.models.TextField(
        "Текст",
        validators=[validate_keywords],
        help_text="Должно содержать слова «превосходно» или «роскошно»",
    )
    category = django.db.models.ForeignKey(
        CatalogCategory,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        verbose_name="Категория",
    )

    tags = django.db.models.ManyToManyField(
        CatalogTag,
        related_name="items",
        blank=True,
        verbose_name="Теги",
    )

    class Meta:
        db_table = "catalog_item"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
