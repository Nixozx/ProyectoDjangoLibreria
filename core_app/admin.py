from django.contrib import admin
from .models import Post, Comentario, Categoria 
from martor.widgets import AdminMartorWidget
from core_app.models import Comentario

admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(Categoria)