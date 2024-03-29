from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Etiqueta(models.Model):
    tag = models.CharField(max_length=20)

    def __str__(self):
         return self.tag

TIPO_PRODUCTO_CHOICES = (
    ('Camiseta', 'Camiseta'),
    ('Short', 'Short'),
    ('Abrigo', 'Abrigo'),
    ('Accesorio', 'Accesorio'),
    ('Pelota', 'Pelota'),
)

class Producto(models.Model):
    codigo = models.CharField(max_length=6)
    nombre = models.CharField(max_length=70)
    etiquetas = models.ManyToManyField(Etiqueta)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=40, choices=TIPO_PRODUCTO_CHOICES)
    imagen = models.ImageField(default="null", upload_to='app/images/')
    precio = models.IntegerField(default=0)

    def __str__(self):
         return self.nombre
    
    class Meta:
         ordering = ["tipo"]

class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
            return f"{self.user} {self.imagen}"
    
    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatares"
    
class Comentario(models.Model):
     autor = models.ForeignKey(User, on_delete=models.CASCADE)
     comment = models.TextField(max_length=1000)
     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
     fecha = models.DateTimeField(default=timezone.now)
     avatar = models.ForeignKey(Avatar, on_delete=models.SET_DEFAULT, default=1)

     def __str__(self):
        return f'{self.autor} en "{self.producto}"'

