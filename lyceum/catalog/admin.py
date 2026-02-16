import django.contrib.admin

import catalog.models


@django.contrib.admin.register(catalog.models.CatalogItem)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@django.contrib.admin.register(catalog.models.CatalogCategory)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "weight", "is_published")
    list_editable = ("is_published", "weight")
    search_fields = ("name",)


@django.contrib.admin.register(catalog.models.CatalogTag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    search_fields = ("name",)
