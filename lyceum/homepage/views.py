__all__ = ()
import http

from django.http import HttpResponse
import django.views
import django.views.generic

import catalog.models
from homepage.forms import EchoForm
import users.models


class HomeView(django.views.generic.TemplateView):
    template_name = "homepage/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = catalog.models.Item.objects.on_main()
        return context


class CoffeeView(django.views.View):
    http_method_names = ["get", "options"]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile, _ = users.models.Profile.objects.get_or_create(
                user=request.user,
            )
            profile.coffee_count += 1
            profile.save(update_fields=["coffee_count"])

        return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)


class EchoView(django.views.generic.FormView):
    form_class = EchoForm
    template_name = "homepage/echo.html"


class EchoSubmitView(django.views.View):
    http_method_names = ["post", "options"]

    def post(self, request, *args, **kwargs):
        form = EchoForm(request.POST)
        if not form.is_valid():
            return HttpResponse("", status=http.HTTPStatus.BAD_REQUEST)

        return HttpResponse(
            form.cleaned_data["text"],
            content_type="text/plain; charset=utf-8",
        )
