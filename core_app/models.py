from django.db import models
from martor.models import MartorField
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#5d3a25')

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    autor = models.CharField(max_length=200, default="Anónimo") 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='portadas/', null=True, blank=True)
    
    # Campos para filtrado
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True, help_text="Para distinguir ediciones")
    editorial = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.autor}"
    
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='posts_fotos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = MartorField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='comentarios_fotos/', blank=True, null=True)

    def __str__(self):
        return f"Comentario de {self.autor.username} en '{self.post.titulo}'"