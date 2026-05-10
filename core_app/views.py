from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required   
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
    return render(request, 'core/home.html')

def catalog(request):
    return render(request, "core/catalog.html")

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

# Solo usuarios logueados pueden entrar aquí
@login_required(login_url='login')
def agregar_libro(request):
    if request.method == 'POST':
         
        return redirect('catalog')
    return render(request, 'core/agregar.html')