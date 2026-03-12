__all__ = ()
from django.contrib import admin

import feedback.models


@admin.register(feedback.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to_status.field.name,
        feedback.models.StatusLog.timestamp.field.name,
    )
    list_select_related = (
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.user.field.name,
    )
    readonly_fields = (
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to_status.field.name,
        feedback.models.StatusLog.timestamp.field.name,
    )


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.status.field.name,
        feedback.models.Feedback.created_on.field.name,
    )
    list_editable = (feedback.models.Feedback.status.field.name,)
    search_fields = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.text.field.name,
    )

    def save_model(self, request, obj, form, change):
        previous_status = None
        if change:
            previous_status = (
                feedback.models.Feedback.objects.filter(pk=obj.pk)
                .values_list(
                    feedback.models.Feedback.status.field.name,
                    flat=True,
                )
                .first()
            )

        super().save_model(request, obj, form, change)

        if change and previous_status and previous_status != obj.status:
            feedback.models.StatusLog.objects.create(
                user=request.user,
                feedback=obj,
                from_status=previous_status,
                to_status=obj.status,
            )
