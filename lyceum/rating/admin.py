__all__ = ()
from django.contrib import admin

import rating.models


@admin.register(rating.models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("item", "user", "value", "updated_at")
    list_filter = ("value", "updated_at")
    search_fields = ("item__name", "user__username", "user__email")
