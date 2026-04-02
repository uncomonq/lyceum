__all__ = ()

import datetime

import django.utils.timezone


def get_request_localdate(request):
    today = django.utils.timezone.localdate()
    offset_value = request.COOKIES.get("timezone_offset")
    if offset_value in (None, ""):
        return today

    try:
        offset_minutes = int(offset_value)
    except ValueError:
        return today

    return (
        django.utils.timezone.now()
        - datetime.timedelta(minutes=offset_minutes)
    ).date()
