from django.urls import path

import catalog.views

urlpatterns = [
    path("", catalog.views.item_list),
    path("<int:item_id>/", catalog.views.item_detail),
]
