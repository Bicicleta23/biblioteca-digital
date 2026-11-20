from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "biblioteca"
urlpatterns = [
    path("", views.lista_libros, name="lista"),
    path("registro/", views.registro, name="registro"),
    path("login/", auth_views.LoginView.as_view(template_name="biblioteca/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("crear/", views.crear_libro, name="crear"),
    path("editar/<int:libro_id>/", views.editar_libro, name="editar"),
    path("eliminar/<int:libro_id>/", views.eliminar_libro, name="eliminar"),
    path("probar-node/",views.probar_microservicio,name="probar_node"),
    path(
    "recomendar/",
    views.recomendar_libro,
    name="recomendar_libro"
),
]
