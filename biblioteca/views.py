from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro
from .forms import LibroForm


def es_gestor(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name="Gestores").exists())


def registro(request):
    if request.user.is_authenticated:
        return redirect("biblioteca:lista")
    formulario = UserCreationForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
        usuario = formulario.save()
        login(request, usuario)
        return redirect("biblioteca:lista")
    return render(request, "biblioteca/registro.html", {"formulario": formulario})


@login_required
def lista_libros(request):
    libros = Libro.objects.all().order_by("titulo")
    return render(request, "biblioteca/lista.html", {"libros": libros, "puede_gestionar": es_gestor(request.user)})


@login_required
@user_passes_test(es_gestor)
def crear_libro(request):
    formulario = LibroForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        messages.success(request, "Libro creado correctamente.")
        return redirect("biblioteca:lista")
    return render(request, "biblioteca/formulario.html", {"formulario": formulario, "accion": "Crear"})


@login_required
@user_passes_test(es_gestor)
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    formulario = LibroForm(request.POST or None, instance=libro)
    if request.method == "POST" and formulario.is_valid():
        formulario.save()
        messages.success(request, "Libro actualizado correctamente.")
        return redirect("biblioteca:lista")
    return render(request, "biblioteca/formulario.html", {"formulario": formulario, "accion": "Editar"})


@login_required
@user_passes_test(es_gestor)
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    if request.method == "POST":
        libro.delete()
        messages.success(request, "Libro eliminado correctamente.")
        return redirect("biblioteca:lista")
    return render(request, "biblioteca/eliminar.html", {"libro": libro})

import os
import requests
from django.http import JsonResponse


def probar_microservicio(request):
    url_base = os.getenv(
        "NODE_SERVICE_URL",
        "http://localhost:3000"
    )

    try:
        respuesta = requests.get(
            f"{url_base}/api/saludo",
            timeout=5
        )
        respuesta.raise_for_status()

        return JsonResponse({
            "django": "Conexión exitosa con Node.js",
            "node": respuesta.json()
        })

    except requests.RequestException:
        return JsonResponse(
            {"error": "No se pudo conectar con Node.js"},
            status=502
        )
        
        

import os
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def recomendar_libro(request):
    recomendacion = None
    error = None
    genero = ""

    if request.method == "POST":
        genero = request.POST.get("genero", "").strip()

        if not genero:
            error = "Debes escribir un género literario."
        else:
            url = os.getenv(
                "NODE_SERVICE_URL",
                "http://localhost:3000"
            )

            try:
                respuesta = requests.post(
                    f"{url}/api/libros/recomendacion",
                    json={"genero": genero},
                    timeout=150
                )
                respuesta.raise_for_status()

                datos = respuesta.json()
                recomendacion = datos.get("recomendacion")

            except requests.RequestException:
                error = "No fue posible obtener la recomendación."

    return render(
        request,
        "biblioteca/recomendar.html",
        {
            "genero": genero,
            "recomendacion": recomendacion,
            "error": error
        }
    )
