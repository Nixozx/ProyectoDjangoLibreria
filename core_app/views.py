from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def catalog(request):
    return render(request, "core/catalog.html")

