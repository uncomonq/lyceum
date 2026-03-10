from django.urls import path

import homepage.views

app_name = "homepage"

urlpatterns = [
    path("", homepage.views.home, name="main"),
    path("coffee/", homepage.views.coffee, name="coffee"),
    path("echo/", homepage.views.echo, name="echo"),
    path("echo/submit/", homepage.views.echo_submit, name="echo_submit"),
]
