from django.contrib import admin

import catalog.models


@admin.register(catalog.models.CatalogItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.CatalogItem._meta.get_field("name").name,
        catalog.models.CatalogItem._meta.get_field("is_published").name,
    )
    list_editable = (
        catalog.models.CatalogItem._meta.get_field("is_published").name,
    )
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@admin.register(catalog.models.CatalogCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.CatalogCategory._meta.get_field("name").name,
        catalog.models.CatalogCategory._meta.get_field("weight").name,
        catalog.models.CatalogCategory._meta.get_field("is_published").name,
    )
    list_editable = (
        catalog.models.CatalogCategory._meta.get_field("weight").name,
        catalog.models.CatalogCategory._meta.get_field("is_published").name,
    )
    search_fields = ("name",)


@admin.register(catalog.models.CatalogTag)
class TagAdmin(admin.ModelAdmin):
    @admin.display(description="Название тега")
    def get_name(self, obj):
        return obj.name

    list_display = (
        catalog.models.CatalogTag._meta.get_field("name").name,
        catalog.models.CatalogTag._meta.get_field("is_published").name,
    )
    list_editable = (
        catalog.models.CatalogTag._meta.get_field("is_published").name,
    )
    search_fields = ("name",)
