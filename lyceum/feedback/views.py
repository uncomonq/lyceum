__all__ = ()
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import (
    apply_bootstrap_classes,
    FeedbackAuthorForm,
    FeedbackFilesForm,
    FeedbackForm,
)
from feedback.models import FeedbackFile


def _build_forms(request):
    if request.method == "POST":
        return (
            apply_bootstrap_classes(FeedbackForm(request.POST)),
            apply_bootstrap_classes(FeedbackAuthorForm(request.POST)),
            apply_bootstrap_classes(
                FeedbackFilesForm(request.POST, request.FILES),
            ),
        )

    return (
        apply_bootstrap_classes(FeedbackForm()),
        apply_bootstrap_classes(FeedbackAuthorForm()),
        apply_bootstrap_classes(FeedbackFilesForm()),
    )


def feedback(request):
    form, author_form, files_form = _build_forms(request)

    if (
        request.method == "POST"
        and form.is_valid()
        and author_form.is_valid()
        and files_form.is_valid()
    ):
        feedback_obj = form.save()

        person = author_form.save(commit=False)
        person.feedback = feedback_obj
        person.save()

        for uploaded_file in files_form.cleaned_data["files"]:
            FeedbackFile.objects.create(
                feedback=feedback_obj,
                file=uploaded_file,
            )

        Path(settings.EMAIL_FILE_PATH).mkdir(parents=True, exist_ok=True)

        send_mail(
            subject="Спасибо за обратную связь",
            message=form.cleaned_data["text"],
            from_email=settings.DJANGO_MAIL,
            recipient_list=[person.mail],
        )
        messages.success(
            request,
            "Форма успешно отправлена.",
        )
        return redirect("feedback:feedback")

    return render(
        request,
        "feedback/feedback.html",
        {
            "form": form,
            "author_form": author_form,
            "files_form": files_form,
        },
    )
