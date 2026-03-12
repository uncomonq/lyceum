__all__ = ()
from django.contrib import admin

import feedback.models


@admin.register(feedback.models.FeedbackPersonData)
class FeedbackPersonDataAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.FeedbackPersonData.name.field.name,
        feedback.models.FeedbackPersonData.mail.field.name,
    )
    search_fields = (
        feedback.models.FeedbackPersonData.name.field.name,
        feedback.models.FeedbackPersonData.mail.field.name,
    )


@admin.register(feedback.models.FeedbackFile)
class FeedbackFileAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.FeedbackFile.feedback.field.name,
        feedback.models.FeedbackFile.file.field.name,
    )


@admin.register(feedback.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.feedback.field.name,
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to.field.name,
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
        feedback.models.StatusLog.to.field.name,
        feedback.models.StatusLog.timestamp.field.name,
    )


def _get_previous_status(feedback_id):
    feedback_model = feedback.models.Feedback
    feedback_obj = feedback_model.objects.only(
        feedback_model.status.field.name,
    ).get(pk=feedback_id)
    return feedback_obj.status


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.person.field.name,
        feedback.models.Feedback.status.field.name,
        feedback.models.Feedback.created_on.field.name,
    )
    list_editable = (feedback.models.Feedback.status.field.name,)
    search_fields = (
        "person__name",
        "person__mail",
        feedback.models.Feedback.text.field.name,
    )

    def save_model(self, request, obj, form, change):
        previous_status = None
        if change:
            previous_status = _get_previous_status(obj.pk)

        super().save_model(request, obj, form, change)

        if not change or not previous_status:
            return

        if previous_status == obj.status:
            return

        feedback.models.StatusLog.objects.create(
            user=request.user,
            feedback=obj,
            from_status=previous_status,
            to=obj.status,
        )
