__all__ = ()
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackAuthorForm, FeedbackFilesForm, FeedbackForm
from feedback.models import FeedbackFile


def feedback(request):
    form = FeedbackForm(request.POST or None)
    author_form = FeedbackAuthorForm(request.POST or None)
    files_form = FeedbackFilesForm(request.POST or None, request.FILES or None)

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
