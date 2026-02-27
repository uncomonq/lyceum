import http

from django.http import HttpResponse
import django.shortcuts

__all__ = ("home", "coffee")

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


def home(request):
    templates = "homepage/main.html"
    return django.shortcuts.render(request, templates, {"items": items})


def coffee(request):
    return HttpResponse("Я чайник", status=http.HTTPStatus.IM_A_TEAPOT)
