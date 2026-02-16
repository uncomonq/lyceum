from django.db import models


class CommonModel(models.Model):
    name = models.CharField(
        "Название",
        max_length=150,
    )
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
    )

    class Meta:
        abstract = True
