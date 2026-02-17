from django.db import models


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
