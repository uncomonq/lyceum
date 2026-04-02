__all__ = ()

import datetime

import django.conf
from django.db.models import Q
import django.utils.timezone

import users.models


def _request_localdate(request):
    timezone_offset = request.COOKIES.get("timezone_offset")
    if timezone_offset is None:
        return django.utils.timezone.localdate()

    try:
        minutes = int(timezone_offset)
    except ValueError:
        return django.utils.timezone.localdate()

    tzinfo = datetime.timezone(datetime.timedelta(minutes=-minutes))
    return django.utils.timezone.now().astimezone(tzinfo).date()


def birthday_users(request):
    today = _request_localdate(request)
    limit = max(django.conf.settings.BIRTHDAY_USERS_LIMIT, 1)
    queryset = (
        users.models.User.objects.active()
        .filter(
            ~Q(email=""),
            profile__birthday__month=today.month,
            profile__birthday__day=today.day,
        )
        .order_by("username")
    )
    total_count = queryset.count()
    queryset = queryset[:limit]

    users_data = []
    for user in queryset:
        users_data.append(
            {
                "name": user.get_full_name() or user.username,
                "email": user.email,
            },
        )

    return {
        "birthday_users": users_data,
        "birthday_users_has_more": total_count > limit,
    }
