__all__ = ("item_list", "item_detail", "return_value_view")
import django.http
import django.shortcuts

import catalog.models


def item_list(request):
    templates = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.filter(is_published=True)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("category__name")
    )
    return django.shortcuts.render(
        request,
        templates,
        {"items": items},
    )


def item_detail(request, pk):
    templates = "catalog/item.html"
    item = django.shortcuts.get_object_or_404(catalog.models.Item, pk=pk)
    return django.shortcuts.render(
        request,
        templates,
        {"item": item},
        )


def item_db_detail(request, pk):
    item = get_object_
    return django.shortcuts.render(
        request,
        "catalog/item.html",
        {"item": item},
    )


def return_value_view(request, number):
    n = int(number)

    if n <= 0:
        raise django.http.Http404

    return django.http.HttpResponse(
        str(n),
        content_type="text/plain; charset=utf-8",
    )
