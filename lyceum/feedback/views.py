__all__ = ()
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm


def feedback(request):
    form = FeedbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        feedback_mail = form.cleaned_data["mail"]
        feedback_text = form.cleaned_data["text"]

        Path(settings.EMAIL_FILE_PATH).mkdir(parents=True, exist_ok=True)

        send_mail(
            subject="Спасибо за обратную связь",
            message=feedback_text,
            from_email=settings.DJANGO_MAIL,
            recipient_list=[feedback_mail],
            fail_silently=True,
        )
        messages.success(
            request,
            "Форма успешно отправлена.",
        )
        return redirect("feedback:feedback")

    return render(request, "feedback/feedback.html", {"form": form})
