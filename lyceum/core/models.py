from django.db import models

__all__ = ("CommonModel",)


class CommonModel(models.Model):
    name = models.CharField(
        "название",
        unique=True,
        max_length=150,
    )
    is_published = models.BooleanField(
        "опубликовано",
        default=True,
        help_text="статус публикации",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]
