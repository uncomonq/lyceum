__all__ = ()
from datetime import timedelta

import django.db.models
import django.http
import django.shortcuts
import django.utils.timezone
from django.utils.translation import gettext_lazy as _

import catalog.models


def item_list(request):
    items = catalog.models.Item.objects.published()

    return _render_item_list(request, items, _("Items catalog"))


def _render_item_list(request, items, title):
    return django.shortcuts.render(
        request,
        "catalog/item_list.html",
        {
            "items": items,
            "page_title": title,
        },
    )


def item_new(request):
    week_ago = django.utils.timezone.now() - timedelta(days=7)
    items = catalog.models.Item.objects.new_items(week_ago)

    return _render_item_list(request, items, _("New items"))


def item_friday(request):
    items = catalog.models.Item.objects.friday_items()

    return _render_item_list(request, items, _("Friday items"))


def item_unverified(request):
    items = catalog.models.Item.objects.unverified_items()

    return _render_item_list(request, items, _("Unverified items"))


def item_detail(request, pk):
    templates = "catalog/item.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.published()
        .select_related("main_image")
        .prefetch_related(
            django.db.models.Prefetch(
                "images",
                queryset=catalog.models.ItemImage.objects.only(
                    "image",
                    "ordering",
                    "item_id",
                ),
            ),
        )
        .only(
            "name",
            "text",
            "category__name",
            "main_image__image",
        ),
        pk=pk,
    )
    main_image = getattr(item, "main_image", None)

    return django.shortcuts.render(
        request,
        templates,
        {"item": item, "main_image": main_image},
    )


def return_value_view(request, number):
    n = int(number)

    if n <= 0:
        raise django.http.Http404

    return django.http.HttpResponse(
        str(n),
        content_type="text/plain; charset=utf-8",
    )
