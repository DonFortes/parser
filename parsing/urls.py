from django.urls import path

from parsing import service

urlpatterns = [
    path("start/", service.main, name="main"),
]
