__all__ = ()

import django.utils.timezone

import users.models


def birthday_users(request):
    today = django.utils.timezone.localdate()
    queryset = users.models.User.objects.active().filter(
        profile__birthday__month=today.month,
        profile__birthday__day=today.day,
    ).order_by("username")

    users_data = [
        {
            "name": user.get_full_name() or user.username,
            "email": user.email,
        }
        for user in queryset
    ]

    return {"birthday_users": users_data}
