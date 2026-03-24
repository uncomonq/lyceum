__all__ = ()
from django.contrib.auth import models as auth_models
from django.db import models


def _set_user_email_unique():
    email_field = auth_models.User._meta.get_field("email")
    email_field._unique = True


_set_user_email_unique()


class UserManager(auth_models.UserManager):
    def get_queryset(self):
        queryset = super().get_queryset()
        profile_related_name = auth_models.User.profile.related.name
        return queryset.select_related(profile_related_name)

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, email):
        normalized_email = self.normalize_email(email)
        return self.active().get(email=normalized_email)


class User(auth_models.User):
    objects = UserManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

    user = models.OneToOneField(
        auth_models.User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name="день рождения",
    )
    image = models.ImageField(
        upload_to=image_path,
        null=True,
        blank=True,
        verbose_name="аватарка",
    )
    coffee_count = models.PositiveIntegerField(
        default=0,
        verbose_name="кол-во кофе",
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"
