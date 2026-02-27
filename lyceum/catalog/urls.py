from django.urls import path

import catalog.views

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path(
        "item/<int:pk>/",
        catalog.views.item_detail,
        name="item_detail_with_prefix",
    ),
    path("<int:pk>/", catalog.views.item_detail, name="item_detail"),
]
