from django.shortcuts import render, redirect
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
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})