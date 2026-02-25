from django.contrib import admin

from catalog.models import Category, Item, Tag


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        Item.name.field.name,
        Item.is_published.field.name,
    )
    list_editable = (Item.is_published.field.name,)
    list_display_links = (Item.name.field.name,)
    filter_horizontal = (Item.tags.field.name,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        Category.name.field.name,
        Category.weight.field.name,
        Category.is_published.field.name,
    )
    list_editable = (
        Category.weight.field.name,
        Category.is_published.field.name,
    )
    prepopulated_fields = {
        Category.slug.field.name: (Category.name.field.name,),
    }
    search_fields = (Category.name.field.name,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    @admin.display(description="Название тега")
    def get_name(self, obj):
        return obj.name

    list_display = (
        "get_name",
        Tag.is_published.field.name,
    )
    list_editable = (Tag.is_published.field.name,)
    search_fields = (Tag.name.field.name,)
