from django.urls import path

import download.views

urlpatterns = [
    path(
        "<path:file_path>",
        download.views.download_media,
        name="download_media",
    ),
]
