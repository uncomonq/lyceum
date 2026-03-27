from django.urls import path

import site_statistics.views

app_name = "statistics"

urlpatterns = [
    path(
        "users/",
        site_statistics.views.UserStatisticsView.as_view(),
        name="users",
    ),
    path(
        "items/",
        site_statistics.views.ItemStatisticsView.as_view(),
        name="items",
    ),
    path(
        "my-items/",
        site_statistics.views.UserRatedItemsView.as_view(),
        name="my_items",
    ),
]
