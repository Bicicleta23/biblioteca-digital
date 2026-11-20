from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
urlpatterns = [
    path("", lambda request: redirect("biblioteca:lista")),
    path("admin/", admin.site.urls),
    path("perros/", include("perros.urls")),
    path("loro/", include("loro.urls")),
    path("polls/", include("polls.urls")),
    path("biblioteca/", include("biblioteca.urls")),
]
