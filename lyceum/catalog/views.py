import django.http


def item_list(request):
    return django.http.HttpResponse("<body>Список элементов</body>")


def item_detail(request, item_id):
    return django.http.HttpResponse("<body>Подробно элемент</body>")
