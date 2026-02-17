from django.contrib import admin

from catalog.models import CatalogCategory, CatalogItem, CatalogTag


@admin.register(CatalogItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        CatalogItem.name.field.name,
        CatalogItem.is_published.field.name,
    )
    list_editable = (CatalogItem.is_published.field.name,)
    list_display_links = (CatalogItem.name.field.name,)
    filter_horizontal = (CatalogItem.tags.field.name,)


@admin.register(CatalogCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        CatalogCategory.name.field.name,
        CatalogCategory.weight.field.name,
        CatalogCategory.is_published.field.name,
    )
    list_editable = (
        CatalogCategory.weight.field.name,
        CatalogCategory.is_published.field.name,
    )
    prepopulated_fields = {
        CatalogCategory.slug.field.name: (CatalogCategory.name.field.name,),
    }
    search_fields = (CatalogCategory.name.field.name,)


@admin.register(CatalogTag)
class TagAdmin(admin.ModelAdmin):
    @admin.display(description="Название тега")
    def get_name(self, obj):
        return obj.name

    list_display = (
        "get_name",
        CatalogTag.is_published.field.name,
    )
    list_editable = (CatalogTag.is_published.field.name,)
    search_fields = (CatalogTag.name.field.name,)
