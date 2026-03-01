__all__ = ("item_list", "item_detail", "return_value_view")
import django.http
import django.shortcuts

from catalog.static_data import get_catalog_items, get_item_by_pk


def item_list(request):
    templates = "catalog/item_list.html"
    return django.shortcuts.render(
        request,
        templates,
        {"items": get_catalog_items()},
    )


def item_detail(request, pk):
    templates = "catalog/item.html"
    item = get_item_by_pk(pk)
    return django.shortcuts.render(request, templates, {"item": item})


def item_db_detail(request, pk):
    item = get_item_by_pk(pk)
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
