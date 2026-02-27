import django.http
import django.shortcuts

import catalog.models

__all__ = ("item_list", "item_detail", "return_value_view")


def item_list(request):
    templates = "catalog/item_list.html"
    items = catalog.models.Item.objects.all()
    return django.shortcuts.render(request, templates, {"items": items})


def item_detail(request, pk):
    templates = "catalog/item.html"
    item = django.shortcuts.get_object_or_404(catalog.models.Item, pk=pk)
    return django.shortcuts.render(request, templates, {"item": item})


def return_value_view(request, number):
    try:
        n = int(number)
    except (TypeError, ValueError):
        raise django.http.Http404

    if n <= 0:
        raise django.http.Http404

    return django.http.HttpResponse(
        str(n),
        content_type="text/plain; charset=utf-8",
    )
