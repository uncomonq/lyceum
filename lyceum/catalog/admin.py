import django.contrib.admin

import catalog.models

DEFAULT_DISPLAY = ("name", "is_published")
DEFAULT_EDITABLE = ("is_published",)


@django.contrib.admin.register(catalog.models.CatalogItem)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = DEFAULT_DISPLAY
    list_editable = DEFAULT_EDITABLE
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@django.contrib.admin.register(catalog.models.CatalogCategory)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "weight", "is_published")
    list_editable = ("is_published", "weight")
    search_fields = ("name",)


@django.contrib.admin.register(catalog.models.CatalogTag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = DEFAULT_DISPLAY
    list_editable = DEFAULT_EDITABLE
    search_fields = ("name",)
