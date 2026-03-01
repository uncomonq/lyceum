__all__ = ("ItemAdmin", "CategoryAdmin", "TagAdmin")
from django.contrib import admin

import catalog.models


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
