__all__ = (
    "item_list",
    "item_new",
    "item_friday",
    "item_unverified",
    "item_detail",
    "download_media",
    "return_value_view",
)
from datetime import timedelta
import mimetypes


from django.conf import settings
import django.db.models
import django.http
import django.shortcuts
import django.utils.timezone

import catalog.models


def item_list(request):
    items = catalog.models.Item.objects.published()

    return _render_item_list(request, items, "Items catalog")


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

    return _render_item_list(request, items, "Новинки")


def item_friday(request):
    items = catalog.models.Item.objects.friday_items()

    return _render_item_list(request, items, "Пятница")


def item_unverified(request):
    items = catalog.models.Item.objects.unverified_items()

    return _render_item_list(request, items, "Непроверенное")


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


def download_media(request, file_path):
    media_root = settings.MEDIA_ROOT.resolve()
    media_path = (settings.MEDIA_ROOT / file_path).resolve()

    try:
        media_path.relative_to(media_root)
    except ValueError as error:
        raise django.http.Http404 from error

    if not media_path.is_file():
        raise django.http.Http404

    content_type, _ = mimetypes.guess_type(str(media_path))
    response = django.http.FileResponse(
        media_path.open("rb"),
        as_attachment=True,
        filename=media_path.name,
        content_type=content_type or "application/octet-stream",
    )

    return response


def return_value_view(request, number):
    n = int(number)

    if n <= 0:
        raise django.http.Http404

    return django.http.HttpResponse(
        str(n),
        content_type="text/plain; charset=utf-8",
    )
