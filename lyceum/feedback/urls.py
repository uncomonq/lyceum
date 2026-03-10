from django.urls import path

from feedback.views import feedback

app_name = "feedback"

urlpatterns = [
    path("", feedback, name="feedback"),
]
