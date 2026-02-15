from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
