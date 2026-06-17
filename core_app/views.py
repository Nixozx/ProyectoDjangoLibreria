from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required   
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Libro, Categoria
from .models import Post, Comentario
from .forms import PostForm, ComentarioForm, CategoriaForm


def home(request):
    return render(request, 'core/home.html')

def catalog(request):
     
    libros_db = Libro.objects.all()
    categorias = Categoria.objects.all()

     
    categoria_id = request.GET.get('categoria')
    editorial_query = request.GET.get('editorial')
    isbn_query = request.GET.get('isbn', '')

     
    if categoria_id:
        libros_db = libros_db.filter(categoria_id=categoria_id)
    
    if editorial_query:
         
        libros_db = libros_db.filter(editorial__icontains=editorial_query)
    
    if isbn_query:

        libros_db = libros_db.filter(isbn__icontains=isbn_query)

     
    return render(request, "core/catalog.html", {
        "libros": libros_db,
        "categorias": categorias,
        "categoria_seleccionada": categoria_id,
        "editorial_query": editorial_query,
        'isbn_query': isbn_query,
    })

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
    categorias = Categoria.objects.all().order_by('nombre')  
    
    context = {
        'total_libros': total_libros,
        'libros': libros,
        'categorias': categorias,  
    }
    return render(request, 'core/dashboard.html', context)

def crear_categoria(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('dashboard') 
    else:
        form = CategoriaForm()
        
    return render(request, 'core/categoriacrear.html', {'form': form})

def eliminar_categoria(request, categoria_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('home')
        
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('dashboard')  

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
        autor_libro = request.POST.get('autor')   
        precio_libro = request.POST.get('precio')
        imagen_libro = request.FILES.get('imagen')
        editorial_libro = request.POST.get('editorial')
        isbn_libro = request.POST.get('isbn')
        categoria_id = request.POST.get('categoria')

        categoria_seleccionada = None
        if categoria_id:
            categoria_seleccionada = Categoria.objects.get(id=categoria_id)

        nuevo_libro = Libro(
            nombre=nombre_libro,
            autor=autor_libro,               
            precio=precio_libro,
            imagen=imagen_libro,
            editorial=editorial_libro,       
            isbn=isbn_libro,                
            categoria=categoria_seleccionada 
        )
        nuevo_libro.save()

        return redirect('catalog')
    
    categorias_db = Categoria.objects.all()
    return render(request, 'core/agregar.html', {'categorias': categorias_db})

def foro_home(request):
    posts = Post.objects.all().order_by('-fecha_creacion')
    return render(request, 'core/foro.html', {'posts': posts})


@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) 
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user 
            post.save()
            return redirect('foro_home') 
    else:
        form = PostForm()
    
    return render(request, 'core/foroadd.html', {'form': form})

def detalle_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all().order_by('fecha_creacion') 
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        form = ComentarioForm(request.POST, request.FILES) 
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post        
            comentario.autor = request.user 
            comentario.save()
            return redirect('detalle_post', post_id=post.id)
    else:
        form = ComentarioForm() 

    return render(request, 'core/detallepost.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form
    })