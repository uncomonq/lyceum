__all__ = ()
from pathlib import Path
import tempfile

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse

from feedback.forms import FeedbackAuthorForm, FeedbackFilesForm, FeedbackForm
from feedback.models import Feedback, FeedbackFile, FeedbackPersonData


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    ALLOW_REVERSE=False,
)
class FeedbackViewsTests(TestCase):
    def test_feedback_page_contains_form_in_context(self):
        response = self.client.get(reverse("feedback:feedback"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("author_form", response.context)
        self.assertIn("files_form", response.context)
        self.assertIsInstance(response.context["form"], FeedbackForm)
        self.assertIsInstance(
            response.context["author_form"],
            FeedbackAuthorForm,
        )
        self.assertIsInstance(
            response.context["files_form"],
            FeedbackFilesForm,
        )

    def test_feedback_form_has_expected_labels_and_help_texts(self):
        form = FeedbackForm()
        author_form = FeedbackAuthorForm()

        self.assertEqual(author_form.fields["name"].label, "Имя")
        self.assertEqual(author_form.fields["mail"].label, "Почта")
        self.assertEqual(form.fields["text"].label, "Текст обращения")

        self.assertEqual(
            author_form.fields["name"].help_text,
            "Укажите ваше имя.",
        )
        self.assertEqual(
            author_form.fields["mail"].help_text,
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

    def test_feedback_form_creates_feedback_record_in_db(self):
        self.client.post(
            reverse("feedback:feedback"),
            {
                "name": "Иван",
                "mail": "ivan@example.com",
                "text": "Спасибо за проект!",
            },
        )

        feedback_obj = Feedback.objects.get()
        self.assertEqual(feedback_obj.person.name, "Иван")
        self.assertEqual(feedback_obj.person.mail, "ivan@example.com")
        self.assertEqual(feedback_obj.text, "Спасибо за проект!")

    def test_feedback_form_allows_file_upload(self):
        uploaded_file = SimpleUploadedFile(
            "test.txt",
            b"feedback attachment",
            content_type="text/plain",
        )

        with tempfile.TemporaryDirectory() as media_dir:
            with override_settings(MEDIA_ROOT=media_dir):
                self.client.post(
                    reverse("feedback:feedback"),
                    {
                        "name": "Иван",
                        "mail": "ivan@example.com",
                        "text": "Спасибо за проект!",
                        "files": uploaded_file,
                    },
                )

                feedback_obj = Feedback.objects.get()
                attached_file = FeedbackFile.objects.get(feedback=feedback_obj)
                self.assertTrue(
                    attached_file.file.name.startswith(
                        f"uploads/{feedback_obj.pk}/",
                    ),
                )
                self.assertTrue(Path(attached_file.file.path).exists())

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
        self.assertIn("author_form", response.context)
        self.assertFormError(
            response.context["author_form"],
            "mail",
            "Введите правильный адрес электронной почты.",
        )


@override_settings(ALLOW_REVERSE=False)
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


@override_settings(ALLOW_REVERSE=False)
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

    def test_admin_creates_status_log_on_status_change(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            username="admin2",
            password="pass12345",
            email="admin2@example.com",
        )
        self.client.force_login(user)

        feedback_obj = Feedback.objects.create(
            text="Текст",
        )
        FeedbackPersonData.objects.create(
            feedback=feedback_obj,
            name="Иван",
            mail="ivan@example.com",
        )

        response = self.client.post(
            reverse("admin:feedback_feedback_change", args=[feedback_obj.pk]),
            {
                "text": feedback_obj.text,
                "status": "in_progress",
                "person-TOTAL_FORMS": "1",
                "person-INITIAL_FORMS": "1",
                "person-MIN_NUM_FORMS": "0",
                "person-MAX_NUM_FORMS": "1",
                "person-0-id": str(feedback_obj.person.pk),
                "person-0-feedback": str(feedback_obj.pk),
                "person-0-name": feedback_obj.person.name,
                "person-0-mail": feedback_obj.person.mail,
                "files-TOTAL_FORMS": "0",
                "files-INITIAL_FORMS": "0",
                "files-MIN_NUM_FORMS": "0",
                "files-MAX_NUM_FORMS": "1000",
                "_save": "Save",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        feedback_obj.refresh_from_db()
        self.assertEqual(feedback_obj.status, "in_progress")
        status_log = feedback_obj.status_logs.get()
        self.assertEqual(status_log.user, user)
        self.assertEqual(status_log.from_status, "received")
        self.assertEqual(status_log.to, "in_progress")
