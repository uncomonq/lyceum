__all__ = ()
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
import django.db.models
import django.utils.safestring
import sorl.thumbnail
import tinymce.models

import catalog.managers
import catalog.utils
import catalog.validators
import core.models


class Tag(core.models.NormalizedNameModel):

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(core.models.NormalizedNameModel):
    weight = django.db.models.PositiveSmallIntegerField(
        "вес",
        default=100,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ],
        help_text="От 1 до 32767",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["weight"]


class Item(core.models.CommonModel):
    objects = catalog.managers.ItemManager()
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
