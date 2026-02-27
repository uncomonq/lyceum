import django.http
import django.shortcuts

__all__ = ("item_list", "item_detail", "return_value_view")


items = [
    {
        "pk": 1,
        "name": "Роскошная лампа",
        "slug": "roskoshnaya-lampa",
        "image": "img/lamp.jpeg",
        "short": "Элегантная лампа для гостиной.",
        "desc": "Самая яркая лампа в нашем каталоге! Роскошная лампа"
        " с изысканным дизайном, выполненная из высококачественных материалов."
        " Идеально подходит для создания уютной атмосферы"
        " в гостиной или спальне.",
    },
    {
        "pk": 2,
        "name": "Стильная подушка",
        "slug": "stilnaya-podushka",
        "image": "img/pillow.jpeg",
        "short": "Мягкая и приятная на ощупь.",
        "desc": "Ортопедическая подушка с высококачественным наполнителем,"
        " стильный дизайн, идеально подходит для отдыха и сна.",
    },
    {
        "pk": 3,
        "name": "Классический ковер",
        "slug": "klassicheskiy-kover",
        "image": "img/carpet.jpg",
        "short": "Тёплый ковер для дома.",
        "desc": "Ковер выполнен из натуральной шерсти, обладает высокой"
        " износостойкостью и приятной текстурой. Идеально подходит для "
        "создания уютной атмосферы в гостиной или спальне.",
    },
]


def item_list(request):
    templates = "catalog/item_list.html"
    return django.shortcuts.render(request, templates, {"items": items})


def item_detail(request, pk):
    templates = "catalog/item.html"
    item = next((item for item in items if item["pk"] == pk), None)
    if item is None:
        raise django.http.Http404
    return django.shortcuts.render(request, templates, {"item": item})


def return_value_view(request, number):
    number_int = int(number)
    return django.http.HttpResponse(
        str(number_int),
        content_type="text/plain; charset=utf-8",
    )
