from django.urls import path
from . import views

urlpatterns = [
    # Define tus rutas aquí

    path("", views.loritos, name="loro"),
   
]

