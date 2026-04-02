__all__ = ()

from django.conf import settings
from django.db import models

import catalog.models


class Rating(models.Model):
    class Value(models.IntegerChoices):
        HATE = 1, "Ненависть"
        DISLIKE = 2, "Неприязнь"
        NEUTRAL = 3, "Нейтрально"
        ADORE = 4, "Обожание"
        LOVE = 5, "Любовь"

    item = models.ForeignKey(
        catalog.models.Item,
        on_delete=models.CASCADE,
        related_name="ratings",
        related_query_name="rating",
        verbose_name="товар",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
        related_query_name="rating",
        verbose_name="пользователь",
    )
    value = models.PositiveSmallIntegerField(
        "оценка",
        choices=Value.choices,
    )
    created_at = models.DateTimeField("создано", auto_now_add=True)
    updated_at = models.DateTimeField("обновлено", auto_now=True)

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
        constraints = [
            models.UniqueConstraint(
                fields=["item", "user"],
                name="unique_rating_per_item_user",
            ),
        ]

    def __str__(self):
        return f"{self.user} → {self.item}: {self.get_value_display()}"
