__all__ = ()
import http

from django.http import HttpResponse
import django.shortcuts
from django.views.decorators.http import require_http_methods, require_POST

import catalog.models
from homepage.forms import EchoForm


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


@require_http_methods(["GET"])
def echo(request):
    form = EchoForm()
    return django.shortcuts.render(
        request,
        "homepage/echo.html",
        {"form": form},
    )


@require_POST
def echo_submit(request):
    form = EchoForm(request.POST)
    if not form.is_valid():
        return HttpResponse("", status=http.HTTPStatus.BAD_REQUEST)

    return HttpResponse(
        form.cleaned_data["text"],
        content_type="text/plain; charset=utf-8",
    )
