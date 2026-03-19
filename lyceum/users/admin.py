__all__ = ()
from django.contrib import admin
import django.contrib.admin.sites
import django.contrib.auth
import django.contrib.auth.admin
import django.contrib.auth.forms

import users.models

User = django.contrib.auth.get_user_model()


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = User
        fields = "__all__"


class ProfileInlined(admin.TabularInline):
    model = users.models.Profile
    can_delete = False
    extra = 0
    readonly_fields = ("coffee_count",)


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    form = UserChangeForm
    inlines = (ProfileInlined,)


try:
    admin.site.unregister(User)
except django.contrib.admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)
