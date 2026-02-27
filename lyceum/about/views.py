import django.shortcuts

__all__ = ("description",)


def description(request):
    return django.shortcuts.render(request, "about/about.html")
