__all__ = ()
from django.contrib import admin
import django.contrib.auth.admin
import django.contrib.auth.models

import users.models


class ProfileInlined(admin.TabularInline):
    model = users.models.Profile
    can_delete = False


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInlined,)


admin.site.unregister(
    django.contrib.auth.models.User,
)

admin.site.register(
    django.contrib.auth.models.User,
    UserAdmin,
)
