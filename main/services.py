from main.models import UserProfile, Inmueble, Comuna, Imagen, Region
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.db import connection
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from data.sinonimos import sinomimos 

def crear_inmueble(nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio_mensual_arriendo:int, tipo_de_inmueble:str, comuna_cod:str, rut_propietario:str, imagen:object):
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
        propietario = propietario,
        imagen = imagen
    )
    return True

def editar_inmueble(inmueble_id:int, nombre:str, descripcion:str, m2_construidos:int, m2_totales:int, num_estacionamientos:int, num_habitaciones:int, num_baños:int, direccion:str, precio_mensual_arriendo:int, tipo_de_inmueble:str, comuna:str, rut_propietario:str, imagen:object):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    comuna = Comuna.objects.get(cod=comuna)
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
    inmueble.imagen = imagen
    inmueble.save()
    return True


def eliminar_inmueble(inmueble_id):
    Inmueble.objects.get(id=inmueble_id).delete()
    return True

from django.contrib.auth.models import User
from main.models import UserProfile

def crear_user(username, first_name, last_name, email, password, password_confirm, direccion, rol, telefono):
    # Verificar si las contraseñas coinciden
    if password != password_confirm:
        raise ValueError("Las contraseñas no coinciden")
    
    # Verificar si el nombre de usuario ya existe
    if User.objects.filter(username=username).exists():
        raise ValueError("El nombre de usuario ya está en uso")
    
    # Verificar si el correo electrónico ya está registrado
    if User.objects.filter(email=email).exists():
        raise ValueError("El correo electrónico ya está en uso")
    
    # Crear el usuario
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    
    # Solo crear el UserProfile si no existe
    UserProfile.objects.get_or_create(
        user=user, 
        defaults={
            'direccion': direccion,
            'rol': rol,
            'telefono_personal': telefono
        }
    )

    return user

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
        messages.error(request, 'Las contraseñas no coinciden')
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

def buscar_propiedad(busqueda):
    if busqueda in sinomimos:
        busqueda = sinomimos[busqueda]
    elif busqueda is None:  
        return Inmueble.objects.all().order_by('comuna')
    
    # Buscador por palabras
    palabras = busqueda.split()
    if 'en' in palabras:
        if len(palabras) <= 2: # En caso que escriba de la forma: "en iquique"
            comuna = palabras[1]
            return Inmueble.objects.filter(Q(comuna__nombre__icontains=comuna))
        else:
            tipo_de_inmueble = palabras[0]
            if tipo_de_inmueble in sinomimos:
                tipo_de_inmueble = sinomimos[tipo_de_inmueble]
            comuna = palabras[2]
            return Inmueble.objects.filter(Q(tipo_de_inmueble__icontains=tipo_de_inmueble) & Q(comuna__nombre__icontains=comuna) ).order_by('comuna')
    else:
        return Inmueble.objects.filter(Q(nombre__icontains=busqueda) | Q(tipo_de_inmueble__icontains=busqueda) | Q(descripcion__icontains=busqueda) | Q(comuna__nombre__icontains=busqueda)).order_by('comuna')

def save_image(img_file:str):
    imagen = Imagen.objects.create(
        img_file = img_file
    )
    return imagen


def filtro_comuna_region(comuna_cod, region_cod, tipo_inmueble):
    query = Q() # Se crear un objeto Q vacío para acumular los filtros

    if tipo_inmueble:
        query &= Q(tipo_de_inmueble__icontains=tipo_inmueble)

    if comuna_cod:
        comuna = Comuna.objects.get(cod=comuna_cod)
        query &= Q(comuna=comuna)
    elif region_cod:
        region = Region.objects.get(cod=region_cod)
        comunas = Comuna.objects.filter(region=region)
        query &= Q(comuna__in=comunas)

    if not query:
        return Inmueble.objects.all()

    # Si llega, se retornan los filtros acomulados
    return Inmueble.objects.filter(query).order_by('comuna')

def obtener_perfil_usuario(user):
    # Intentar obtener el perfil de usuario, crearlo si no existe
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile