from django.db import models

class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    autor = models.CharField(max_length=200, default="Anónimo") 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='portadas/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.autor}"