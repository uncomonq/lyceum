from django.contrib import admin

import catalog.models

COMMON_DISPLAY = ("name", "is_published")
COMMON_EDITABLE = ("is_published",)
CATEGORY_DISPLAY = ("name", "weight", "is_published")
CATEGORY_EDITABLE = ("weight", "is_published")


@admin.register(catalog.models.CatalogItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = COMMON_DISPLAY
    list_editable = COMMON_EDITABLE
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


@admin.register(catalog.models.CatalogCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = CATEGORY_DISPLAY
    list_editable = CATEGORY_EDITABLE
    search_fields = ("name",)


@admin.register(catalog.models.CatalogTag)
class TagAdmin(admin.ModelAdmin):
    @admin.display(description="Название тега")
    def get_name(self, obj):
        return obj.name

    list_display = ("get_name", "is_published")
    list_editable = COMMON_EDITABLE
    search_fields = ("name",)
