from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm


def feedback(request):
    form = FeedbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        feedback_item = form.save()
        send_mail(
            subject="Спасибо за обратную связь",
            message=feedback_item.text,
            from_email=settings.DJANGO_MAIL,
            recipient_list=[feedback_item.mail],
        )
        messages.success(
            request,
            "Форма успешно отправлена.",
        )
        return redirect("feedback:feedback")

    return render(request, "feedback/feedback.html", {"form": form})
