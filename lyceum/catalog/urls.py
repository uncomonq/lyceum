from django.urls import path, register_converter

import catalog.views
from .converters import PositiveIntWithLeadingZerosConverter

register_converter(PositiveIntWithLeadingZerosConverter, "posint")


urlpatterns = [
    path("", catalog.views.item_list),
    path("<int:item_id>/", catalog.views.item_detail),
    path("re/<posint:number>/", catalog.views.return_value_view),
    path("converter/<posint:number>/", catalog.views.return_value_view),
]
