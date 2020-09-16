from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name="page"),
    path("wiki/<str:name>/edit", views.editpage, name="edit"),
    path("save/<str:name>", views.save, name="save"),
    path("searchwiki", views.searchwiki, name="searchwiki"),
    path("random", views.randompage, name="randompage"),
    path("new", views.newpage, name="newpage"),
    path("error/<str:args>", views.error, name="error")
]
