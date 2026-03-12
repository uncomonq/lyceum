__all__ = ()
from django.conf import settings
from django.db import models


def feedback_upload_to(instance, filename):
    return f"uploads/{instance.feedback_id}/{filename}"


class FeedbackPersonData(models.Model):
    name = models.CharField(
        "имя",
        max_length=50,
    )
    mail = models.EmailField(
        "почта",
        max_length=254,
    )

    class Meta:
        verbose_name = "данные отправителя"
        verbose_name_plural = "данные отправителей"

    def __str__(self):
        return self.name


class Feedback(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "получено"
        IN_PROGRESS = "in_progress", "в обработке"
        ANSWERED = "answered", "ответ дан"

    person = models.ForeignKey(
        FeedbackPersonData,
        on_delete=models.CASCADE,
        blank=True,
        related_name="feedbacks",
        verbose_name="данные отправителя",
    )
    text = models.TextField(
        "текст",
    )
    created_on = models.DateTimeField(
        "дата и время создания",
        auto_now_add=True,
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
        return self.person.name


class FeedbackFile(models.Model):
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="обратная связь",
    )
    file = models.FileField(
        "файл",
        upload_to=feedback_upload_to,
    )

    class Meta:
        verbose_name = "файл обратной связи"
        verbose_name_plural = "файлы обратной связи"


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
    to = models.CharField(
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
        return f"{self.feedback_id}: {self.from_status} -> {self.to}"
