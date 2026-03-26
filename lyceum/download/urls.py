from django.urls import path

import download.views

urlpatterns = [
    path(
        "<path:file_path>",
        download.views.DownloadMediaView.as_view(),
        name="download_media",
    ),
]
