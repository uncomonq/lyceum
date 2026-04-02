__all__ = ()

from django.contrib.auth import models as auth_models
from django.db import models


class UserManager(auth_models.UserManager):
    def get_queryset(self):
        queryset = super().get_queryset()
        profile_related_name = auth_models.User.profile.related.name
        return queryset.select_related(profile_related_name)

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def normalize_email(self, email):
        normalized_email = super().normalize_email(email)
        local_part, separator, domain_part = normalized_email.partition("@")
        local_part = local_part.lower()
        domain_part = domain_part.lower()
        local_part = local_part.split("+", maxsplit=1)[0]

        if domain_part in {"ya.ru", "yandex.ru"}:
            domain_part = "yandex.ru"
            local_part = local_part.replace(".", "-")
        elif domain_part == "gmail.com":
            local_part = local_part.replace(".", "")

        if not separator:
            return local_part

        return f"{local_part}@{domain_part}"


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
    attempts_count = models.PositiveIntegerField(
        default=0,
        verbose_name="кол-во неудачных входов",
    )
    blocked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="заблокирован с",
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"
