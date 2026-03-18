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

    @patch("users.views.timezone.now")
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

    @patch("users.views.timezone.now")
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
            response, f"{login_url}?next={reverse('users:profile')}",
        )

    def test_profile_update(self):
        self.client.login(
            username="active_user", password="strong_password_123",
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


class CoffeeCounterTests(TestCase):
    def test_coffee_counter_increments_for_authenticated_user(self):
        user = User.objects.create_user(
            username="coffee_user",
            password="strong_password_123",
            is_active=True,
        )
        Profile.objects.create(user=user)

        self.client.login(
            username="coffee_user", password="strong_password_123",
        )
        self.client.get(reverse("homepage:coffee"))

        user.profile.refresh_from_db()
        self.assertEqual(user.profile.coffee_count, 1)
