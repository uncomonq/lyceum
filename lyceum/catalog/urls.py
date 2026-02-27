from django.urls import path, re_path

import catalog.views

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("<int:pk>/", catalog.views.item_detail, name="item_detail"),
    re_path(
        r"^re/(?P<number>0*[1-9][0-9]*)/$",
        catalog.views.return_value_view,
        name="re",
    ),
]
