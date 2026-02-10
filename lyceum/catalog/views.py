from django.http import Http404, HttpResponse

from catalog.converters import positive_int_converter


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, item_id):
    return HttpResponse("<body>Подробно элемент</body>")


def re(request, number):
    return HttpResponse(number)


def converter_view(request, number: str):
    result = positive_int_converter(number)
    if result is None:
        raise Http404("Invalid number")
    return HttpResponse(str(result))
