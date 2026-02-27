import http

from django.http import HttpResponse
import django.shortcuts

import catalog.models

__all__ = ("home", "coffee")


def home(request):
    templates = "homepage/main.html"
    items = catalog.models.Item.objects.filter(is_published=True)[:3]
    return django.shortcuts.render(request, templates, {"items": items})


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)
