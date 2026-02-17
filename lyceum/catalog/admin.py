from django.contrib import admin

import catalog.models


@admin.register(catalog.models.CatalogItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@admin.register(catalog.models.CatalogCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "weight", "is_published")
    list_editable = ("weight", "is_published")
    search_fields = ("name",)


@admin.register(catalog.models.CatalogTag)
class TagAdmin(admin.ModelAdmin):
    @admin.display(description="Название тега")
    def get_name(self, obj):
        return obj.name

    list_display = ("get_name", "is_published")
    list_editable = ("is_published",)
    search_fields = ("name",)
