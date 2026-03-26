__all__ = ()
import datetime
from http import HTTPStatus
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings, TestCase
from django.urls import reverse
from django.utils import timezone

import users.models

User = get_user_model()


@override_settings(
    DEFAULT_USER_IS_ACTIVE=False,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class SignUpAndActivationTests(TestCase):
    def test_signup_creates_inactive_user_profile_and_email(self):
        response = self.client.post(
            reverse("users:signup"),
            {
                "username": "new_user",
                "password1": "strong_password_123",
                "password2": "strong_password_123",
            },
        )

        self.assertRedirects(response, reverse("users:login"))

        user = User.objects.get(username="new_user")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(
            users.models.Profile.objects.filter(user=user).exists(),
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/auth/activate/new_user/", mail.outbox[0].body)

    @patch("django.utils.timezone.now")
    def test_activation_works_in_12_hours(self, mocked_now):
        user = User.objects.create_user(
            username="valid_user",
            password="strong_password_123",
            is_active=False,
        )
        mocked_now.return_value = user.date_joined + datetime.timedelta(
            hours=11,
            minutes=59,
        )

        response = self.client.get(
            reverse("users:activate", kwargs={"username": user.username}),
        )

        self.assertRedirects(response, reverse("users:login"))
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    @patch("django.utils.timezone.now")
    def test_activation_fails_after_12_hours(self, mocked_now):
        user = User.objects.create_user(
            username="expired_user",
            password="strong_password_123",
            is_active=False,
        )
        mocked_now.return_value = user.date_joined + datetime.timedelta(
            hours=12,
            seconds=1,
        )

        response = self.client.get(
            reverse("users:activate", kwargs={"username": user.username}),
        )

        self.assertRedirects(response, reverse("users:login"))
        user.refresh_from_db()
        self.assertFalse(user.is_active)


@override_settings(ALLOW_REVERSE=False)
class UserPagesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="active_user",
            email="active_user@example.com",
            password="strong_password_123",
            is_active=True,
            first_name="",
            last_name="",
        )
        self.profile = users.models.Profile.objects.create(
            user=self.user,
            birthday=datetime.date(2000, 1, 10),
        )

    def test_user_list_has_only_active_users(self):
        inactive_user = User.objects.create_user(
            username="inactive_user_on_list",
            email="inactive_user_on_list@example.com",
            password="strong_password_123",
            is_active=False,
        )
        users.models.Profile.objects.create(user=inactive_user)

        response = self.client.get(reverse("users:user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, inactive_user.username)
        self.assertContains(response, "10.01")

    def test_user_detail_shows_fallback_for_empty_name(self):
        response = self.client.get(
            reverse("users:user_detail", kwargs={"pk": self.user.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "не указано")
        self.assertContains(response, str(self.profile.coffee_count))

    def test_profile_requires_login(self):
        response = self.client.get(reverse("users:profile"))
        login_url = reverse("users:login")
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('users:profile')}",
        )

    def test_profile_page_has_coffee_button(self):
        self.client.login(
            username="active_user",
            password="strong_password_123",
        )
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("homepage:coffee"))

    def test_profile_update(self):
        self.client.login(
            username="active_user",
            password="strong_password_123",
        )
        response = self.client.post(
            reverse("users:profile"),
            {
                "email": "mail@example.com",
                "first_name": "Имя",
                "last_name": "Фамилия",
                "birthday": "2000-01-10",
            },
        )

        self.assertRedirects(response, reverse("users:profile"))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(self.user.email, "mail@example.com")
        self.assertEqual(self.user.first_name, "Имя")
        self.assertEqual(self.profile.birthday, datetime.date(2000, 1, 10))

    def test_logout_requires_post_and_finishes_session(self):
        self.client.login(
            username="active_user",
            password="strong_password_123",
        )

        get_response = self.client.get(reverse("users:logout"))
        self.assertEqual(get_response.status_code, 405)

        post_response = self.client.post(reverse("users:logout"))
        self.assertRedirects(post_response, reverse("users:login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_inactive_user_sees_activation_error_on_login(self):
        inactive_user = User.objects.create_user(
            username="inactive_user",
            email="inactive_user@example.com",
            password="strong_password_123",
            is_active=False,
        )

        response = self.client.post(
            reverse("users:login"),
            {
                "username": inactive_user.username,
                "password": "strong_password_123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Аккаунт не активирован")


@override_settings(ALLOW_REVERSE=False)
class LoginByMailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="mail_user",
            email="mail_user@example.com",
            password="strong_password_123",
            is_active=True,
        )
        users.models.Profile.objects.create(user=self.user)

    def test_user_can_login_by_mail(self):
        response = self.client.post(
            reverse("users:login"),
            {
                "username": self.user.email,
                "password": "strong_password_123",
            },
        )
        self.assertRedirects(response, reverse("users:profile"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_middleware_replaces_request_user_with_proxy_model(self):
        self.client.login(
            username="mail_user",
            password="strong_password_123",
        )
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.wsgi_request.user, users.models.User)

    def test_duplicate_mail_is_not_allowed_on_profile_update(self):
        second_user = User.objects.create_user(
            username="second_user",
            email="second@example.com",
            password="strong_password_123",
            is_active=True,
        )
        users.models.Profile.objects.create(user=second_user)

        self.client.login(
            username="mail_user",
            password="strong_password_123",
        )
        response = self.client.post(
            reverse("users:profile"),
            {
                "email": "second@example.com",
                "first_name": "Имя",
                "last_name": "Фамилия",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Пользователь с такой почтой уже существует.",
        )

    def test_profile_update_does_not_change_coffee_count(self):
        self.user.profile.coffee_count = 9
        self.user.profile.save(update_fields=["coffee_count"])
        self.client.login(
            username="mail_user",
            password="strong_password_123",
        )
        response = self.client.post(
            reverse("users:profile"),
            {
                "email": "mail_user@example.com",
                "first_name": "Имя",
                "last_name": "Фамилия",
                "coffee_count": 999,
            },
        )

        self.assertRedirects(response, reverse("users:profile"))
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.coffee_count, 9)


class CoffeeCounterTests(TestCase):
    def test_coffee_counter_increments_for_authenticated_user(self):
        user = User.objects.create_user(
            username="coffee_user",
            password="strong_password_123",
            is_active=True,
        )
        users.models.Profile.objects.create(user=user)

        self.client.login(
            username="coffee_user",
            password="strong_password_123",
        )
        self.client.get(reverse("homepage:coffee"))

        user.profile.refresh_from_db()
        self.assertEqual(user.profile.coffee_count, 1)


@override_settings(ALLOW_REVERSE=False)
class EmailNormalizationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="normalize_user",
            email="normalize_user@example.com",
            password="strong_password_123",
            is_active=True,
        )
        users.models.Profile.objects.create(user=self.user)

    def test_yandex_domain_is_canonicalized(self):
        self.client.login(
            username="normalize_user",
            password="strong_password_123",
        )
        response = self.client.post(
            reverse("users:profile"),
            {
                "email": "Name.Tag+spam@Ya.Ru",
                "first_name": "Имя",
                "last_name": "Фамилия",
            },
        )

        self.assertRedirects(response, reverse("users:profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "name-tag@yandex.ru")

    def test_gmail_dots_are_ignored(self):
        self.client.login(
            username="normalize_user",
            password="strong_password_123",
        )
        response = self.client.post(
            reverse("users:profile"),
            {
                "email": "Na.Me+tag@gmail.com",
                "first_name": "Имя",
                "last_name": "Фамилия",
            },
        )

        self.assertRedirects(response, reverse("users:profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "name@gmail.com")


@override_settings(
    ALLOW_REVERSE=False,
    MAX_AUTH_ATTEMPTS=2,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class AuthAttemptsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="attempt_user",
            email="attempt_user@example.com",
            password="strong_password_123",
            is_active=True,
        )
        users.models.Profile.objects.create(user=self.user)

    def test_user_is_deactivated_after_max_failed_attempts(self):
        login_url = reverse("users:login")
        self.client.post(
            login_url,
            {"username": "attempt_user", "password": "wrong_password"},
        )
        self.client.post(
            login_url,
            {"username": "attempt_user", "password": "wrong_password"},
        )

        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(self.user.profile.attempts_count, 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/auth/reactivate/attempt_user/", mail.outbox[0].body)

    @patch("django.utils.timezone.now")
    def test_reactivation_link_works_in_one_week(self, mocked_now):
        blocked_at = timezone.make_aware(datetime.datetime(2026, 3, 1, 12, 0))
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        self.user.profile.blocked_at = blocked_at
        self.user.profile.attempts_count = 2
        self.user.profile.save(update_fields=["blocked_at", "attempts_count"])

        mocked_now.return_value = blocked_at + datetime.timedelta(
            days=6,
            hours=23,
        )
        response = self.client.get(
            reverse(
                "users:reactivate",
                kwargs={"username": self.user.username},
            ),
        )

        self.assertRedirects(response, reverse("users:login"))
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.profile.attempts_count, 0)
        self.assertIsNone(self.user.profile.blocked_at)


@override_settings(ALLOW_REVERSE=False)
class BirthdayUsersContextProcessorTests(TestCase):
    @patch("users.context_processors.django.utils.timezone.localdate")
    def test_context_processor_returns_only_active_users_with_today_birthday(
        self,
        mocked_localdate,
    ):
        mocked_localdate.return_value = datetime.date(2026, 3, 26)

        birthday_user = User.objects.create_user(
            username="birthday_user",
            email="birthday@example.com",
            password="strong_password_123",
            is_active=True,
            first_name="Именинник",
            last_name="Первый",
        )
        users.models.Profile.objects.create(
            user=birthday_user,
            birthday=datetime.date(1995, 3, 26),
        )

        inactive_birthday_user = User.objects.create_user(
            username="inactive_birthday",
            email="inactive@example.com",
            password="strong_password_123",
            is_active=False,
        )
        users.models.Profile.objects.create(
            user=inactive_birthday_user,
            birthday=datetime.date(1994, 3, 26),
        )

        other_day_user = User.objects.create_user(
            username="other_day",
            email="other@example.com",
            password="strong_password_123",
            is_active=True,
        )
        users.models.Profile.objects.create(
            user=other_day_user,
            birthday=datetime.date(1993, 3, 25),
        )

        response = self.client.get(reverse("homepage:main"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context["birthday_users"],
            [
                {
                    "name": "Именинник Первый",
                    "email": "birthday@example.com",
                },
            ],
        )

    @patch("users.context_processors.django.utils.timezone.localdate")
    def test_birthday_block_is_rendered_in_base_template(
        self,
        mocked_localdate,
    ):
        mocked_localdate.return_value = datetime.date(2026, 3, 26)

        birthday_user = User.objects.create_user(
            username="birthday_user_for_template",
            email="template@example.com",
            password="strong_password_123",
            is_active=True,
            first_name="Шаблон",
            last_name="Проверка",
        )
        users.models.Profile.objects.create(
            user=birthday_user,
            birthday=datetime.date(2001, 3, 26),
        )

        response = self.client.get(reverse("homepage:main"))

        self.assertContains(response, "Именниники сегодня:")
        self.assertContains(response, "Шаблон Проверка")
        self.assertContains(response, "template@example.com")
