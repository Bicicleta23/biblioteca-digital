from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Libro

class BibliotecaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user("lector", password="PruebaSegura123!")
        self.gestor = User.objects.create_user("gestor", password="PruebaSegura123!")
        grupo, _ = Group.objects.get_or_create(name="Gestores")
        self.gestor.groups.add(grupo)
        self.libro = Libro.objects.create(titulo="Libro prueba", autor="Autor", disponible=True)

    def test_requiere_login(self):
        r = self.client.get(reverse("biblioteca:lista"))
        self.assertEqual(r.status_code, 302)

    def test_lector_no_puede_crear(self):
        self.client.force_login(self.usuario)
        self.assertNotEqual(self.client.get(reverse("biblioteca:crear")).status_code, 200)

    def test_gestor_crud(self):
        self.client.force_login(self.gestor)
        self.client.post(reverse("biblioteca:crear"), {"titulo":"Nuevo", "autor":"A", "disponible":"on"})
        nuevo = Libro.objects.get(titulo="Nuevo")
        self.client.post(reverse("biblioteca:editar", args=[nuevo.pk]), {"titulo":"Editado", "autor":"B"})
        nuevo.refresh_from_db()
        self.assertEqual(nuevo.titulo, "Editado")
        self.client.post(reverse("biblioteca:eliminar", args=[nuevo.pk]))
        self.assertFalse(Libro.objects.filter(pk=nuevo.pk).exists())
