from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("searchPage/", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.randomPage, name="randomPage"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
]
