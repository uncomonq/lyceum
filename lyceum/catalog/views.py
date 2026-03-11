__all__ = ()
from datetime import timedelta

import django.shortcuts
import django.utils.timezone

import catalog.models

ITEMS_CONTEXT_KEY = "items"
ITEM_CONTEXT_KEY = "item"
MAIN_IMAGE_CONTEXT_KEY = "main_image"
ITEM_LIST_TEMPLATE = "catalog/item_list.html"
ITEM_DETAIL_TEMPLATE = "catalog/item.html"


def item_list(request):
    items = catalog.models.Item.objects.published()
    return django.shortcuts.render(
        request,
        ITEM_LIST_TEMPLATE,
        {
            ITEMS_CONTEXT_KEY: items,
            "page_title": "Catalog",
        },
    )


def item_detail(request, pk):
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.published(),
        pk=pk,
    )

    main_image = getattr(item, "main_image", None)

    return django.shortcuts.render(
        request,
        ITEM_DETAIL_TEMPLATE,
        {
            ITEM_CONTEXT_KEY: item,
            MAIN_IMAGE_CONTEXT_KEY: main_image,
        },
    )


def item_new(request):
    from_datetime = django.utils.timezone.now() - timedelta(days=7)
    items = catalog.models.Item.objects.new_items(from_datetime)

    return django.shortcuts.render(
        request,
        ITEM_LIST_TEMPLATE,
        {
            ITEMS_CONTEXT_KEY: items,
            "page_title": "New items",
        },
    )


def item_friday(request):
    items = catalog.models.Item.objects.friday_items()

    return django.shortcuts.render(
        request,
        ITEM_LIST_TEMPLATE,
        {
            ITEMS_CONTEXT_KEY: items,
            "page_title": "Friday Items",
        },
    )


def item_unverified(request):
    items = catalog.models.Item.objects.unverified_items()

    return django.shortcuts.render(
        request,
        ITEM_LIST_TEMPLATE,
        {
            ITEMS_CONTEXT_KEY: items,
            "page_title": "Unverified Items",
        },
    )
