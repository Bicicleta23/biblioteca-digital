# Biblioteca Digital - Entrega 2

## Funcionalidades
Registro público, login/logout, catálogo para usuarios autenticados, CRUD restringido a personal `is_staff` o grupo `Gestores`, Django Admin y pruebas automatizadas.

## Ejecutar en Windows
1. `py -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py crear_roles`
6. `python manage.py createsuperuser`
7. `python manage.py runserver`
8. Abre http://127.0.0.1:8000/biblioteca/ ; en `/admin/` asigna el grupo Gestores a usuarios que podrán modificar libros.

## Docker (requiere Docker Desktop)
1. Copia `.env.example` a `.env` y define `DJANGO_SECRET_KEY` segura. Para generar una clave: `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
2. `docker compose up --build`
3. En otra terminal: `docker compose exec web python manage.py createsuperuser`
4. Abre http://localhost:8000/biblioteca/

## Pruebas
`python manage.py test biblioteca`

## Despliegue
Despliega desde un repositorio privado o público en una plataforma que admita Docker; configura `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` y `DJANGO_CSRF_TRUSTED_ORIGINS` con el dominio real. Usa almacenamiento persistente para SQLite o migra a PostgreSQL antes de producción. El despliegue remoto NO está realizado en este paquete.

## Seguridad y datos
La base de datos original se excluyó para no distribuir cuentas o datos existentes. El arranque Docker ejecuta las migraciones y crea el grupo Gestores. Nunca subas `.env` al repositorio. Las rutas de otras apps se conservaron.
