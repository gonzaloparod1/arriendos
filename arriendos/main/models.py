import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class UserProfile(models.Model):
    roles = (
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
        ('admin', 'Admin')
    )
    direccion = models.CharField(max_length=255, blank=False)
    telefono_personal = models.CharField(max_length=20, null=True)
    rol = models.CharField(max_length=50, default='arrendatario', choices=roles)
    user = models.OneToOneField(
        User, 
        related_name='userprofile', 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        nombre = self.user.first_name
        apellido = self.user.last_name
        usuario = self.user.username
        rol = self.rol
        return f'{nombre} {apellido} | {usuario} | {rol}'

class Region(models.Model):
    cod = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=255)

class Comuna(models.Model):
    cod = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=255)
    region = models.ForeignKey(
        Region,
        on_delete=models.RESTRICT,
        related_name='comunas'
    )
    def __str__(self):
        nombre = self.nombre
        return f'{nombre}'

class Inmueble(models.Model):
    inmuebles = (
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela')
    )
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=1500)
    m2_construidos = models.IntegerField(validators=[MinValueValidator(1)])
    m2_totales = models.IntegerField(validators=[MinValueValidator(1)]) # o del terrerno
    num_estacionamientos = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    num_habitaciones = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    num_baños = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    direccion = models.CharField(max_length=255)
    precio_mensual_arriendo = models.IntegerField(validators=[MinValueValidator(1000)])
    tipo_de_inmueble = models.CharField(max_length=20, choices=inmuebles)
    comuna = models.ForeignKey(
        Comuna,
        related_name='inmuebles',
        on_delete=models.RESTRICT
    )
    propietario = models.ForeignKey(
        User,
        related_name='inmueble',
        on_delete=models.RESTRICT
    )
    imagen = models.ForeignKey(
        'Imagen',
        related_name='inmueble',
        null= True,
        blank= False,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        nombre = self.nombre
        comuna = self.comuna
        tipo_inmueble = self.tipo_de_inmueble
        return f'{nombre} {comuna} | {tipo_inmueble}'

class Solicitud(models.Model):
    estados = (
        ('pendiente', 'Pendiente'),
        ('rezachaza', 'Rechazada'),
        ('aprobada', 'Aprobada')
    )
    inmueble =  models.ForeignKey(
        Inmueble,
        related_name='solicitudes',
        on_delete=models.CASCADE
    )
    arrendador = models.ForeignKey(
        User,
        related_name='solicitudes',
        on_delete=models.CASCADE 
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=estados)

# Genera un nombre aleatorio para guardar las imágenes
def generar_nombre_aleatorio(instancia, archivo):
    ext = archivo.split('.')[-1]
    nombre_aleatorio = uuid.uuid4().hex
    return f'img/{nombre_aleatorio}.{ext}'

class Imagen(models.Model):
    img_file = models.ImageField(upload_to=generar_nombre_aleatorio, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.img_file
    
    class Meta:
        ordering = ['-created_at']