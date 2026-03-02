__all__ = ("home", "coffee")
import http

import django.db.models
from django.http import HttpResponse
import django.shortcuts

import catalog.models


def home(request):
    templates = "homepage/main.html"
    items = (
        catalog.models.Item.objects.filter(
            is_published=True,
            is_on_main=True,
            category__is_published=True,
        )
        .select_related("category")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only("name"),
            ),
        )
        .order_by("name")
    )
    return django.shortcuts.render(
        request,
        templates,
        {"items": items},
    )


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)
