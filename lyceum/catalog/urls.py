from django.urls import path, re_path, register_converter

import catalog.views
from .converters import PositiveIntWithLeadingZerosConverter

register_converter(PositiveIntWithLeadingZerosConverter, "posint")


urlpatterns = [
    path("", catalog.views.item_list, name="item-list"),
    path(
        "converter/<posint:number>/",
        catalog.views.return_value_view,
        name="item-converter",
    ),
    re_path(
        r"^re/(?P<number>0*[1-9][0-9]*)/$",
        catalog.views.return_value_view,
        name="item-re-check",
    ),
    path("<int:item_id>/", catalog.views.item_detail, name="item-detail"),
]
