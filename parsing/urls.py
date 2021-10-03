from django.urls import path

from parsing import service, views

urlpatterns = [
    path("start/", service.main, name="main"),
    path("", views.index, name="index"),
]
