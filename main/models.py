from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    tipo_de_usuario = (
        ('arrendador', 'Arrendador'),
        ('arrendatario', 'Arrendatario'),
    )
    nombre = models.CharField(max_length=50, blank=False)
    apellido = models.CharField(max_length=50, blank=False)
    rut = models.CharField(max_length=12, blank=False)
    direccion = models.CharField(max_length=255, blank=False)
    telefono_personal = models.CharField(max_length=20, blank=False)
    user_type = models.CharField(max_length=20, choices=tipo_de_usuario)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        nombre = self.nombre
        apellido = self.apellido
        usuario = self.user.username
        tipo_usuario = self.tipo_de_usuario
        return f'{nombre} {apellido} | {usuario} | {tipo_usuario}'


class Inmueble(models.Model):
    inmuebles = (
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela')
    )
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500)
    m2_construidos = models.IntegerField()
    m2_totales = models.IntegerField() # o del terrerno
    cant_estacionamientos = models.IntegerField()
    cant_habitaciones = models.IntegerField()
    cant_banos = models.IntegerField()
    direccion = models.CharField(max_length=255)
    comuna = models.CharField(max_length=50)
    precio_mensual_arriendo = models.IntegerField()
    tipo_de_inmueble = models.CharField(max_length=20, choices=inmuebles)

    def __str__(self):
        nombre = self.nombre
        comuna = self.comuna
        tipo_inmueble = self.tipo_de_inmueble
        return f'{nombre} {comuna} | {tipo_inmueble}'
