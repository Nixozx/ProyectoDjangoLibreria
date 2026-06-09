from django import forms
from .models import Post
from .models import Post, Comentario 

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'categoria', 'contenido', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de tu post'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe aquí tu historia...', 'rows': 5}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido', 'imagen']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una respuesta...', 'rows': 3}),
            }),
        }