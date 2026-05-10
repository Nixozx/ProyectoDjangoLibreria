from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required   
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Libro

def home(request):
    return render(request, 'core/home.html')

def catalog(request):
    libros_db = Libro.objects.all()
    return render(request, "core/catalog.html", {"libros": libros_db})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cuenta creada con éxito!")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='login')
def agregar_libro(request):
    if request.method == 'POST':

        nombre_libro = request.POST.get('nombre')
        precio_libro = request.POST.get('precio')
        imagen_libro = request.FILES.get('imagen')


        nuevo_libro = Libro(
            nombre=nombre_libro,
            precio=precio_libro,
            imagen=imagen_libro
        )
        nuevo_libro.save()

        return redirect('catalog')
    return render(request, 'core/agregar.html')