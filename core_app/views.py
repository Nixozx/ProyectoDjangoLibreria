from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
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


def admin_dashboard(request):

    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('home')

    total_libros = Libro.objects.count()
    libros = Libro.objects.all().order_by('-id')
    
    context = {
        'total_libros': total_libros,
        'libros': libros,
    }
    return render(request, 'core/dashboard.html', context)

def eliminar_libro(request, libro_id):
    if not request.user.is_superuser:
        return redirect('home')
    
    libro = get_object_or_404(Libro, id=libro_id)
    libro.delete()
    return redirect('dashboard')


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