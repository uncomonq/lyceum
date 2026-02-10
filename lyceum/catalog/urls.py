from django.urls import path, re_path

import catalog.views

urlpatterns = [
    path("", catalog.views.item_list),
    path("<int:item_id>/", catalog.views.item_detail),
    re_path(r"^re/(?P<number>[1-9][0-9]*)/$", catalog.views.re),
    re_path(
        r"^converter/(?P<number>[1-9][0-9]*)/$", catalog.views.converter_view
    ),
]
