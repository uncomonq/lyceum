from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, item_id):
    return HttpResponse("<body>Подробно элемент</body>")


def return_value_view(request, number):
    number_int = int(number)
    return HttpResponse(
        str(number_int),
        content_type="text/plain; charset=utf-8",
    )
