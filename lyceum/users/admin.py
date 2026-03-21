__all__ = ()
from django.contrib import admin
import django.contrib.admin.sites
import django.contrib.auth
import django.contrib.auth.admin
import django.contrib.auth.models

import users.forms
import users.models

User = users.models.User


class ProfileInlined(admin.TabularInline):
    model = users.models.Profile
    can_delete = False
    extra = 0
    readonly_fields = ("coffee_count",)


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    form = users.forms.UserChangeForm
    inlines = (ProfileInlined,)


try:
    admin.site.unregister(django.contrib.auth.models.User)
except django.contrib.admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)
