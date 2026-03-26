from django.urls import path

import catalog.views

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.ItemListView.as_view(), name="item_list"),
    path(
        "<int:pk>/",
        catalog.views.ItemDetailView.as_view(),
        name="item_detail",
    ),
    path("new/", catalog.views.ItemNewView.as_view(), name="item_new"),
    path(
        "friday/",
        catalog.views.ItemFridayView.as_view(),
        name="item_friday",
    ),
    path(
        "unverified/",
        catalog.views.ItemUnverifiedView.as_view(),
        name="item_unverified",
    ),
]
