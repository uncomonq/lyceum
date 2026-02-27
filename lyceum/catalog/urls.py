from django.urls import path

import catalog.views

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("<int:pk>/", catalog.views.item_detail, name="item_detail"),
]
