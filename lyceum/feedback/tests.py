__all__ = ()
from pathlib import Path
import tempfile

from django.test import override_settings, TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.models import Feedback


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class FeedbackViewsTests(TestCase):
    def test_feedback_page_contains_form_in_context(self):
        response = self.client.get(reverse("feedback:feedback"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], FeedbackForm)

    def test_feedback_form_has_expected_labels_and_help_texts(self):
        form = FeedbackForm()

        self.assertEqual(form.fields["name"].label, "Имя")
        self.assertEqual(form.fields["mail"].label, "Почта")
        self.assertEqual(form.fields["text"].label, "Текст обращения")

        self.assertEqual(form.fields["name"].help_text, "Укажите ваше имя.")
        self.assertEqual(
            form.fields["mail"].help_text,
            "Укажите почту для обратной связи.",
        )
        self.assertEqual(
            form.fields["text"].help_text,
            "Введите текст обращения.",
        )

    def test_feedback_form_redirects_to_feedback_page_after_submit(self):
        response = self.client.post(
            reverse("feedback:feedback"),
            {
                "name": "Иван",
                "mail": "ivan@example.com",
                "text": "Спасибо за проект!",
            },
        )

        self.assertRedirects(response, reverse("feedback:feedback"))


class FeedbackSendMailTests(TestCase):
    def test_feedback_form_saves_mail_to_send_mail_directory(self):
        file_backend = "django.core.mail.backends.filebased.EmailBackend"

        with tempfile.TemporaryDirectory() as temp_dir:
            with override_settings(
                EMAIL_BACKEND=file_backend,
                EMAIL_FILE_PATH=temp_dir,
            ):
                self.client.post(
                    reverse("feedback:feedback"),
                    {
                        "name": "Иван",
                        "mail": "ivan@example.com",
                        "text": "Текст для письма",
                    },
                )

            files = list(Path(temp_dir).iterdir())

        self.assertEqual(len(files), 1)
        self.assertEqual(Feedback.objects.count(), 1)
