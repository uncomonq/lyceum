from django.urls import path

import catalog.views

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("<int:pk>/", catalog.views.item_detail, name="item_detail"),
    path("new/", catalog.views.item_new, name="item_new"),
    path("friday/", catalog.views.item_friday, name="item_friday"),
    path("unverified/", catalog.views.item_unverified, name="item_unverified"),
]
