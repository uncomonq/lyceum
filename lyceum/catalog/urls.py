from django.urls import path, re_path, register_converter

from catalog.converters import PositiveIntWithLeadingZerosConverter
import catalog.views

register_converter(PositiveIntWithLeadingZerosConverter, "posint")

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("<slug:slug>/", catalog.views.item_detail, name="item_detail"),
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
