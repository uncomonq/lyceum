__all__ = ()
import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings, TestCase
from django.urls import reverse

from users.models import Profile

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
        self.assertTrue(Profile.objects.filter(user=user).exists())

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
            password="strong_password_123",
            is_active=True,
            first_name="",
            last_name="",
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_user_list_has_active_users(self):
        response = self.client.get(reverse("users:user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_user_detail_shows_fallback_for_empty_name(self):
        response = self.client.get(
            reverse("users:user_detail", kwargs={"pk": self.user.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "не указано")

    def test_profile_requires_login(self):
        response = self.client.get(reverse("users:profile"))
        login_url = reverse("users:login")
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('users:profile')}",
        )

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
        Profile.objects.create(user=self.user)

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

    def test_duplicate_mail_is_not_allowed_on_profile_update(self):
        second_user = User.objects.create_user(
            username="second_user",
            email="second@example.com",
            password="strong_password_123",
            is_active=True,
        )
        Profile.objects.create(user=second_user)

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
        Profile.objects.create(user=user)

        self.client.login(
            username="coffee_user",
            password="strong_password_123",
        )
        self.client.get(reverse("homepage:coffee"))

        user.profile.refresh_from_db()
        self.assertEqual(user.profile.coffee_count, 1)
