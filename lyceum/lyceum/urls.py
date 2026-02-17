from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
]

if settings.DEBUG and settings.DEBUG_TOOLBAR_AVAILABLE:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
