from django.conf import settings
import django.conf.urls.static
# import django.contrib.auth.urls
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("admin/", django.contrib.admin.site.urls),
    path("auth/", include(("users.urls", "users"), namespace="users")),
    path("tinymce/", include("tinymce.urls")),
    path("catalog/", include("catalog.urls")),
    path("download/", include("download.urls")),
    path("feedback/", include("feedback.urls")),
]

if settings.DEBUG and settings.DEBUG_TOOLBAR_AVAILABLE:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
    urlpatterns += django.conf.urls.static.static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
