from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path('search/<str:query>', views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/not_found", views.not_found, name="not_found")
]
