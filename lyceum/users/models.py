__all__ = ()
import django.contrib.auth.models
from django.db import models

django.contrib.auth.models.User._meta.ger_field("email")._unique = True


class UserManager(django.contrib.auth.models.UserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                django.contrib.auth.models.User.profile.related.name,
            )
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, email):
        normalized_email = self.normalize_email(email)
        return self.active().get(email=normalized_email)


class User(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

    user = models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=models.CASCADE,
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
