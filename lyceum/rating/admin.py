__all__ = ()
from django.contrib import admin

import rating.models


@admin.register(rating.models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("item", "user", "value", "updated_at")
    list_filter = (
        rating.models.Rating._meta.get_field("value").name,
        rating.models.Rating._meta.get_field("updated_at").name,
    )
    search_fields = (
        f"{rating.models.Rating._meta.get_field('item').name}__name",
        f"{rating.models.Rating._meta.get_field('user').name}__username",
        f"{rating.models.Rating._meta.get_field('user').name}__email",
    )
