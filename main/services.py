from main.models import UserProfile, Inmueble, Comuna
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.db import connection
from django.db.models import Q
from django.contrib import messages

def crear_inmueble(nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio_mensual_arriendo:int, tipo_de_inmueble:str, comuna_cod:str, rut_propietario:str):
    comuna = Comuna.objects.get(cod=comuna_cod)
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

def editar_user_sin_password(username:str, first_name:str, last_name:str, email:str, direccion:str, rol:str, telefono:str=None):
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()
    user_profile = UserProfile.objects.get(user=user)
    user_profile.direccion = direccion
    user_profile.telefono_personal = telefono
    user_profile.rol = rol
    user_profile.save()

def eliminar_user(rut:str):
    eliminar = User.objects.get(username=rut)
    eliminar.delete()

def obtener_propiedades_comunas(filtro):
    if filtro is None:  
        return Inmueble.objects.all().order_by('comuna') # Entrega un objeto, al poner .value() entrega un diccionario
    # Si llegamos, hay un filtro
    return Inmueble.objects.filter(Q(nombre__icontains=filtro) | Q(descripcion__icontains=filtro) ).order_by('comuna')

def obtener_propiedades_regiones(filtro):
    consulta = '''
    select I.nombre, I.descripcion, R.nombre as region from main_inmueble as I
    join main_comuna as C on I.comuna_id = C.cod
    join main_region as R on C.region_id = R.cod
    order by R.cod;
    '''
    if filtro is not None:
        filtro = filtro.lower()
        consulta = f'''
        select I.nombre, I.descripcion, R.nombre as region from main_inmueble as I
        join main_comuna as C on I.comuna_id = C.cod
        join main_region as R on C.region_id = R.cod where lower(I.nombre) like '%{filtro}%' or lower(I.descripcion) like '%{filtro}%'
        order by R.cod;
        '''
    cursor = connection.cursor()
    cursor.execute(consulta)
    registros = cursor.fetchall() # LAZY LOADING
    return registros

def cambio_password(request, password:str, password_repeat:str):
    if password != password_repeat:
        messages.warning(request, 'Las contraseñas no coinciden')
        return
    request.user.set_password(password)
    request.user.save()
    messages.success(request, 'Contraseña actualizada exitosamente')

'''
from django.db.models import F, Q

def obtener_propiedades_regiones(filtro=None):
    # Construye la consulta base
    inmuebles = Inmueble.objects.select_related('comuna__region').annotate(
        region_nombre=F('comuna__region__nombre')
    ).order_by('comuna__region__cod')

    # Aplica el filtro si se proporciona
    if filtro:
        filtro = filtro.lower()
        inmuebles = inmuebles.filter(
            Q(nombre__icontains=filtro) | Q(descripcion__icontains=filtro)
        )

    return inmuebles

# Explicación:
# select_related: Usa select_related para hacer un join implícito con los modelos relacionados (Comuna y Region). 
# Esto optimiza la consulta reduciendo el número de consultas a la base de datos.
# annotate: Añade un campo anotado region_nombre que contiene el nombre de la región.
# order_by: Ordena los resultados por el código de la región.
# Filtro: Si se proporciona un filtro, se usa el método filter con Q para buscar coincidencias
# en el nombre o la descripción, usando icontains para una búsqueda insensible a mayúsculas y minúsculas.

# Uso
# propiedades = obtener_propiedades_regiones(filtro="casa")
# for propiedad in propiedades:
#     print(propiedad.nombre, propiedad.descripcion, propiedad.region_nombre)
'''