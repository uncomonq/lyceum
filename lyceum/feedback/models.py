__all__ = ()
from django.conf import settings
from django.db import models


class Feedback(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "получено"
        IN_PROGRESS = "in_progress", "в обработке"
        ANSWERED = "answered", "ответ дан"

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
    status = models.CharField(
        "статус обработки",
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED,
    )

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.name


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedback_status_logs",
        verbose_name="пользователь",
    )
    timestamp = models.DateTimeField(
        "время изменения",
        auto_now_add=True,
    )
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="status_logs",
        verbose_name="обратная связь",
    )
    from_status = models.CharField(
        "из статуса",
        max_length=20,
        choices=Feedback.Status.choices,
        db_column="from",
    )
    to_status = models.CharField(
        "в статус",
        max_length=20,
        choices=Feedback.Status.choices,
        db_column="to",
    )

    class Meta:
        verbose_name = "лог смены статуса"
        verbose_name_plural = "логи смен статусов"
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.feedback_id}: {self.from_status} -> {self.to_status}"
