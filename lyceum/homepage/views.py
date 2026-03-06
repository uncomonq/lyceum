__all__ = ()
import http

from django.http import HttpResponse
import django.shortcuts

import catalog.models


def home(request):
    templates = "homepage/main.html"
    items = catalog.models.Item.objects.on_main()
    return django.shortcuts.render(
        request,
        templates,
        {"items": items},
    )


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)
