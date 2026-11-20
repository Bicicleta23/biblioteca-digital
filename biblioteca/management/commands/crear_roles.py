from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Crea el grupo Gestores para administrar libros"
    def handle(self, *args, **options):
        grupo, creado = Group.objects.get_or_create(name="Gestores")
        self.stdout.write(self.style.SUCCESS("Grupo Gestores listo. Asigna usuarios desde /admin/."))
