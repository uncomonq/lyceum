import django.http


def description(request):
    return django.http.HttpResponse("<body>О проекте</body>")
