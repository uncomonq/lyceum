__all__ = ()
from django.contrib import admin

import feedback.models


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.created_on.field.name,
    )
    search_fields = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.text.field.name,
    )
