__all__ = ()
from django import forms
from django.contrib.auth import get_user_model
import django.contrib.auth.forms
import django.core.exceptions

import users.models

User = get_user_model()
INACTIVE_USER_ERROR = (
    "Аккаунт не активирован. Проверьте письмо со ссылкой активации."
)


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            css_classes = field.field.widget.attrs.get("class", "")
            field.field.widget.attrs["class"] = (
                f"{css_classes} form-control".strip()
            )


class UserLoginForm(django.contrib.auth.forms.AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = User.objects.filter(username=username).first()

            if (
                user is not None
                and not user.is_active
                and user.check_password(password)
            ):
                raise django.core.exceptions.ValidationError(
                    INACTIVE_USER_ERROR,
                    code="inactive",
                )

        return super().clean()

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise django.core.exceptions.ValidationError(
                INACTIVE_USER_ERROR,
                code="inactive",
            )

        super().confirm_login_allowed(user)


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False, label="Почта")
    first_name = forms.CharField(required=False, label="Имя")
    last_name = forms.CharField(required=False, label="Фамилия")

    class Meta:
        model = users.models.Profile
        fields = ("email", "first_name", "last_name", "birthday", "image")
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["email"].initial = self.user.email
        self.fields["first_name"].initial = self.user.first_name
        self.fields["last_name"].initial = self.user.last_name

        for field in self.visible_fields():
            css_classes = field.field.widget.attrs.get("class", "")
            field.field.widget.attrs["class"] = (
                f"{css_classes} form-control".strip()
            )

    def save(self, commit=True):
        profile = super().save(commit=False)

        self.user.email = self.cleaned_data["email"]
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]

        if commit:
            self.user.save(update_fields=["email", "first_name", "last_name"])
            profile.user = self.user
            profile.save()

        return profile
