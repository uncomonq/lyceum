__all__ = ("home", "coffee")
import http

from django.http import HttpResponse
import django.shortcuts

import catalog.models


def home(request):
    templates = "homepage/main.html"
    items = (
        catalog.models.Item.objects.filter(is_published=True, is_on_main=True)
        .select_related("category")
        .prefetch_related("tags")
        .only("name", "category__name", "text", "tags__name")
        .order_by("name")
    )
    return django.shortcuts.render(
        request,
        templates,
        {"items": items},
    )


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)
