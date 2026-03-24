__all__ = ()
import django
import django.contrib.auth
import django.contrib.auth.forms
import django.core.exceptions
import django.forms

import users.models


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class UserCreationForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.username.field.name,
            "password1",
            "password2",
        )


class UserLoginForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.AuthenticationForm,
):
    inactive_error_message = "Аккаунт не активирован"

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            auth_username = username
            if "@" in username:
                try:
                    auth_username = users.models.User.objects.by_mail(
                        username,
                    ).username
                except users.models.User.DoesNotExist:
                    auth_username = username

            self.user_cache = django.contrib.auth.authenticate(
                self.request,
                username=auth_username,
                password=password,
            )

            if self.user_cache is None:
                user = users.models.User.objects.filter(
                    username=auth_username,
                ).first()
                if (
                    user
                    and user.check_password(password)
                    and not user.is_active
                ):

                    raise django.forms.ValidationError(
                        self.inactive_error_message,
                        code="inactive",
                    )

                raise self.get_invalid_login_error()

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserChangeForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserChangeForm,
):
    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.email.field.name,
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
        )

    def clean_email(self):
        email = self.cleaned_data.get(users.models.User.email.field.name)
        normalized_email = users.models.User.objects.normalize_email(email)

        queryset = users.models.User.objects.exclude(pk=self.instance.pk)
        if queryset.filter(email=normalized_email).exists():
            raise django.core.exceptions.ValidationError(
                "Пользователь с такой почтой уже существует.",
            )

        return normalized_email


class UpdateProfileForm(
    BootstrapFormMixin,
    django.forms.ModelForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[users.models.Profile.coffee_count.field.name].disabled = (
            True
        )

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.birthday.field.name,
            users.models.Profile.image.field.name,
            users.models.Profile.coffee_count.field.name,
        )
        help_texts = {
            users.models.Profile.birthday.field.name: "Формат: гг.мм.дд",
        }
