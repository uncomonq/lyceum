__all__ = ()

import django.conf

import users.models
import users.utils


def birthday_users(request):
    today = users.utils.get_request_localdate(request)
    queryset = (
        users.models.User.objects.active()
        .filter(
            profile__birthday__month=today.month,
            profile__birthday__day=today.day,
        )
        .order_by("username")
    )
    limit = django.conf.settings.BIRTHDAY_USERS_LIMIT
    if limit > 0:
        queryset = queryset[:limit]

    users_data = [
        {
            "name": user.get_full_name() or user.username,
            "email": user.email or "Email не указан",
        }
        for user in queryset
    ]

    return {"birthday_users": users_data}
