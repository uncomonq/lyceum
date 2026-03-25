__all__ = ()

import datetime

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone

import users.models


class UserAuthBackend(ModelBackend):
    lock_duration = datetime.timedelta(weeks=1)

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        try:
            user = self._get_user_for_login(username)
        except users.models.User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            self._reset_attempts(user)
            return user

        self._register_failed_attempt(request, user)
        return None

    def _get_user_for_login(self, username):
        if "@" in username:
            return users.models.User.objects.by_mail(username)

        return users.models.User.objects.active().get(username=username)

    def _register_failed_attempt(self, request, user):
        if not hasattr(user, "profile"):
            return

        profile = user.profile
        profile.attempts_count += 1
        update_fields = ["attempts_count"]

        if profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
            user.is_active = False
            user.save(update_fields=["is_active"])

            profile.blocked_at = timezone.now()
            update_fields.append("blocked_at")
            self._send_reactivation_email(request, user)

        profile.save(update_fields=update_fields)

    def _reset_attempts(self, user):
        if not hasattr(user, "profile"):
            return

        profile = user.profile
        if profile.attempts_count != 0 or profile.blocked_at is not None:
            profile.attempts_count = 0
            profile.blocked_at = None
            profile.save(update_fields=["attempts_count", "blocked_at"])

    def _send_reactivation_email(self, request, user):
        activate_url = reverse(
            "users:reactivate",
            kwargs={"username": user.username},
        )
        if request is not None:
            activate_url = request.build_absolute_uri(activate_url)

        send_mail(
            f"Здравствуй {user.username}",
            "Перейди по ссылке для активации аккаунта " f"{activate_url}",
            settings.DJANGO_MAIL,
            [user.email or settings.DJANGO_MAIL],
            fail_silently=False,
        )
