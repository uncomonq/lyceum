from django.http import HttpResponse
import django.shortcuts

items = [
    {
        "id": 1,
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
        "id": 2,
        "name": "Стильная подушка",
        "slug": "stilnaya-podushka",
        "image": "img/pillow.jpeg",
        "short": "Мягкая и приятная на ощупь.",
        "desc": "Ортопедическая подушка с высококачественным наполнителем,"
        " стильный дизайн, идеально подходит для отдыха и сна.",
    },
    {
        "id": 3,
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


def item_detail(request, slug):
    templates = "catalog/item.html"
    item = next((i for i in items if i["slug"] == slug), None)
    return django.shortcuts.render(request, templates, {"item": item})


def return_value_view(request, number):
    number_int = int(number)
    return HttpResponse(
        str(number_int),
        content_type="text/plain; charset=utf-8",
    )
