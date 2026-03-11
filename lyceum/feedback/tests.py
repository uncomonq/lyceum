__all__ = ()
from pathlib import Path
import tempfile

from django.contrib.auth import get_user_model
from django.core import mail
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

    def test_feedback_form_submits_without_name(self):
        response = self.client.post(
            reverse("feedback:feedback"),
            {
                "name": "",
                "mail": "ivan@example.com",
                "text": "Спасибо за проект!",
            },
        )

        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_feedback_form_redirect_displays_success_message(self):
        response = self.client.post(
            reverse("feedback:feedback"),
            {
                "name": "Иван",
                "mail": "ivan@example.com",
                "text": "Спасибо за проект!",
            },
            follow=True,
        )

        self.assertContains(response, "Форма успешно отправлена.")

    def test_feedback_form_invalid_data_shows_form_errors(self):
        response = self.client.post(
            reverse("feedback:feedback"),
            {
                "name": "Иван",
                "mail": "not-an-email",
                "text": "Текст",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertFormError(
            response.context["form"],
            "mail",
            "Введите правильный адрес электронной почты.",
        )


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
            saved_mail_content = files[0].read_text(encoding="utf-8")

        self.assertEqual(len(files), 1)
        self.assertIn("Текст для письма", saved_mail_content)
        self.assertEqual(Feedback.objects.count(), 1)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_feedback_form_uses_text_as_email_body(self):
        self.client.post(
            reverse("feedback:feedback"),
            {
                "name": "Иван",
                "mail": "ivan@example.com",
                "text": "Тело письма",
            },
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].body, "Тело письма")
        self.assertEqual(mail.outbox[0].from_email, "noreply@example.com")
        self.assertEqual(mail.outbox[0].to, ["ivan@example.com"])


class FeedbackAdminTests(TestCase):
    def test_feedback_model_visible_in_admin_index(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            username="admin",
            password="pass12345",
            email="admin@example.com",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feedback")
