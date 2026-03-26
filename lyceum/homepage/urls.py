from django.urls import path

import homepage.views

app_name = "homepage"

urlpatterns = [
    path("", homepage.views.HomeView.as_view(), name="main"),
    path("coffee/", homepage.views.CoffeeView.as_view(), name="coffee"),
    path("echo/", homepage.views.EchoView.as_view(), name="echo"),
    path(
        "echo/submit/",
        homepage.views.EchoSubmitView.as_view(),
        name="echo_submit",
    ),
]
