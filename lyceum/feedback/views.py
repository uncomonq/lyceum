__all__ = ()
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
import django.shortcuts
import django.views

from feedback.forms import FeedbackAuthorForm, FeedbackFilesForm, FeedbackForm
from feedback.models import FeedbackFile


class FeedbackView(django.views.View):
    template_name = "feedback/feedback.html"

    def _build_forms(self, request):
        form = FeedbackForm(request.POST or None)
        author_form = FeedbackAuthorForm(request.POST or None)
        files_form = FeedbackFilesForm(
            request.POST or None,
            request.FILES or None,
        )

        return form, author_form, files_form

    def get(self, request, *args, **kwargs):
        form, author_form, files_form = self._build_forms(request)
        return django.shortcuts.render(
            request,
            self.template_name,
            {
                "form": form,
                "author_form": author_form,
                "files_form": files_form,
            },
        )

    def post(self, request, *args, **kwargs):
        form, author_form, files_form = self._build_forms(request)
        if (
            form.is_valid()
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
            return django.shortcuts.redirect("feedback:feedback")

        return django.shortcuts.render(
            request,
            self.template_name,
            {
                "form": form,
                "author_form": author_form,
                "files_form": files_form,
            },
        )
