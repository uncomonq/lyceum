from django.contrib import admin
import django.db.models
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail
from tinymce.widgets import TinyMCE

import catalog.models

__all__ = ("ItemAdmin", "CategoryAdmin", "TagAdmin")


class MainImageInline(admin.StackedInline):
    model = catalog.models.MainImage
    extra = 0
    max_num = 1


class ItemImageInline(admin.TabularInline):
    model = catalog.models.ItemImage
    extra = 1


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        "main_image_preview",
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = (MainImageInline, ItemImageInline)

    formfield_overrides = {
        django.db.models.TextField: {
            "widget": TinyMCE(
                attrs={"cols": 80, "rows": 20},
                mce_attrs={
                    "menubar": False,
                    "plugins": "lists link table code",
                    "toolbar": (
                        "undo redo | formatselect | bold italic | "
                        "alignleft aligncenter alignright | "
                        "bullist numlist | link table | removeformat"
                    ),
                },
            ),
        },
    }

    def main_image_preview(self, obj):
        if not hasattr(obj, "main_image"):
            return "—"

        thumb = get_thumbnail(
            obj.main_image.image,
            "300x300",
            crop="center",
            quality=80,
        )

        return format_html(
            '<img src="{}" width="60" height="60"'
            ' style="object-fit:cover;" />',
            thumb.url,
        )

    main_image_preview.short_description = "Главное изображение"


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.weight.field.name,
        catalog.models.Category.is_published.field.name,
    )
    list_editable = (
        catalog.models.Category.weight.field.name,
        catalog.models.Category.is_published.field.name,
    )
    prepopulated_fields = {
        catalog.models.Category.slug.field.name: (
            catalog.models.Category.name.field.name,
        ),
    }
    search_fields = (catalog.models.Category.name.field.name,)


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
    )
    list_editable = (catalog.models.Tag.is_published.field.name,)
    search_fields = (catalog.models.Tag.name.field.name,)
