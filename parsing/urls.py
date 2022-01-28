from django.urls import path

from parsing import service, views

urlpatterns = [
    path("start/", views.main, name="main"),
    path("", views.index, name="index"),
]
