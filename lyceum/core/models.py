__all__ = ("CommonModel", "NormalizedNameModel")

from django.core.exceptions import ValidationError
import django.db.models

from catalog.utils import normalize_name


class CommonModel(django.db.models.Model):
    name = django.db.models.CharField(
        "название",
        unique=True,
        max_length=150,
    )
    is_published = django.db.models.BooleanField(
        "опубликовано",
        default=True,
        help_text="статус публикации",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class NormalizedNameModel(CommonModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        help_text="Должен содержать только латинские буквы, цифры,"
        " дефисы и знаки подчёркивания",
    )
    normalized_name = django.db.models.CharField(
        "normalized_name",
        max_length=200,
        null=False,
        blank=False,
        editable=False,
        unique=False,
        error_messages={"unique": "Объект с похожим именем уже существует."},
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name or "")
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        norm = normalize_name(self.name)
        self.normalized_name = norm

        qs = self.__class__.objects.filter(normalized_name=norm)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                {"name": "Объект с похожим именем уже существует."},
            )
