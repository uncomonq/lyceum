__all__ = ("home", "coffee")
import http

from django.http import HttpResponse
import django.shortcuts

from catalog.static_data import get_catalog_items


def home(request):
    templates = "homepage/main.html"
    return django.shortcuts.render(
        request,
        templates,
        {"items": get_catalog_items()[:3]},
    )


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)
