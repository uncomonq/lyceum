from django.db import models


class Feedback(models.Model):
    name = models.CharField(
        "название",
        max_length=50,
    )
    text = models.TextField(
        "текст",
    )
    created_at = models.DateTimeField(
        "дата создания",
        auto_now_add=True,
    )
