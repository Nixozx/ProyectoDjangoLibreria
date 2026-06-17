from django import forms

from .models import Post, Comentario,Categoria
from martor.fields import MartorFormField

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'categoria', 'contenido', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de tu post'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe aquí tu historia...', 'rows': 5}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'color']
        labels = {
            'nombre': 'Nombre de la Categoría',
            'color': 'Color (Hexadecimal)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. Gastos, Tareas...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control', 
                'type': 'color'  
            }),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido', 'imagen']
        widgets = {
            'contenido': MartorFormField(),
        }
        