__all__ = ("description",)
import django.shortcuts


def description(request):
    return django.shortcuts.render(request, "about/about.html")
