from main.models import UserProfile, Inmueble, Comuna
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

def crear_inmueble(nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio_mensual_arriendo:int, tipo_de_inmueble:str, comuna:str, rut_propietario:str):
    comuna = Comuna.objects.get(nombre=comuna)
    propietario = User.objects.get(username=rut_propietario)
    Inmueble.objects.create(
        nombre = nombre,
        descripcion = descripcion,
        m2_construidos = m2_construidos,
        m2_totales = m2_totales,
        num_estacionamientos = num_estacionamientos,
        num_habitaciones = num_habitaciones,
        num_baños = num_baños,
        direccion = direccion,
        precio_mensual_arriendo = precio_mensual_arriendo,
        tipo_de_inmueble = tipo_de_inmueble,
        comuna = comuna,
        propietario = propietario
    )

def editar_inmueble(inmueble_id:int, nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio_mensual_arriendo:int, tipo_de_inmueble:str, comuna:str, rut_propietario:str):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    comuna = Comuna.objects.get(nombre=comuna)
    propietario = User.objects.get(username=rut_propietario)
    inmueble.nombre = nombre
    inmueble.descripcion = descripcion
    inmueble.m2_construidos = m2_construidos
    inmueble.m2_totales = m2_totales
    inmueble.num_estacionamientos = num_estacionamientos
    inmueble.num_habitaciones = num_habitaciones
    inmueble.num_baños = num_baños
    inmueble.direccion = direccion
    inmueble.precio_mensual_arriendo = precio_mensual_arriendo
    inmueble.tipo_de_inmueble = tipo_de_inmueble
    inmueble.comuna = comuna
    inmueble.propietario = propietario
    inmueble.save()


def eliminar_inmueble(inmueble_id):
    eliminar = Inmueble.objects.get(id=inmueble_id)
    eliminar.delete()

def crear_user(username:str, first_name:str, last_name:str, email:str, password:str, pass_confirm:str, direccion:str, telefono:str=None) -> list[bool, str]:
    if password != pass_confirm:
        return False, 'Las contraseñas no coinciden'
    try:
        user = User.objects.create_user(
            username,
            email,
            password,
            first_name=first_name,
            last_name=last_name,
        )
    except IntegrityError:
        return False, 'Rut duplicado'
    UserProfile.objects.create(
        direccion=direccion,
        telefono_personal=telefono,
        user=user
    )
    return True

def editar_user(username:str, first_name:str, last_name:str, email:str, password:str, pass_confirm:str, direccion:str, telefono:str=None):
    # 1. Nos traemos el user y modificamos sus datos
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.set_password(password)
    user.save()
    # 2. Nos traemosel UserProfile y modificamos su datos
    user_profile = UserProfile.objects.get(user=user)
    user_profile.direccion = direccion
    user_profile.telefono_personal = telefono
    user_profile.save()

def eliminar_user(rut:str):
    eliminar = User.objects.get(username=rut)
    eliminar.delete()