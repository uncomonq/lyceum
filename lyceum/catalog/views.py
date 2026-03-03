__all__ = ("item_list", "item_detail", "return_value_view")
import django.db.models
import django.http
import django.shortcuts

import catalog.models


def item_list(request):
    templates = "catalog/item_list.html"
    items = catalog.models.Item.objects.published()
    return django.shortcuts.render(
        request,
        templates,
        {"items": items},
    )


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
                    "alt",
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
            "main_image__alt",
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
