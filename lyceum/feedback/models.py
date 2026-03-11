__all__ = ()
from django.db import models


class Feedback(models.Model):
    name = models.CharField(
        "имя",
        max_length=50,
    )
    text = models.TextField(
        "текст",
    )
    created_on = models.DateTimeField(
        "дата и время создания",
        auto_now_add=True,
    )
    mail = models.EmailField(
        "почта",
        max_length=254,
    )

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.name
