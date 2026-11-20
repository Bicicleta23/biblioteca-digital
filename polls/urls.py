from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),

    path("gatito/", views.gatito, name="gatito"),
    path("moto/", views.moto, name="moto"),
    path("pez/", views.pez, name="pez"),
    path("perros/", views.perros, name="perros"),

    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]