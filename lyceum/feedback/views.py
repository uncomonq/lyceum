__all__ = ()
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm
from feedback.models import FeedbackFile


def feedback(request):
    form = FeedbackForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        feedback_obj = form.save()

        for uploaded_file in form.cleaned_data["files"]:
            FeedbackFile.objects.create(
                feedback=feedback_obj,
                file=uploaded_file,
            )

        feedback_mail = feedback_obj.person.mail
        feedback_text = form.cleaned_data["text"]

        Path(settings.EMAIL_FILE_PATH).mkdir(parents=True, exist_ok=True)

        send_mail(
            subject="Спасибо за обратную связь",
            message=feedback_text,
            from_email=settings.DJANGO_MAIL,
            recipient_list=[feedback_mail],
        )
        messages.success(
            request,
            "Форма успешно отправлена.",
        )
        return redirect("feedback:feedback")

    return render(request, "feedback/feedback.html", {"form": form})
