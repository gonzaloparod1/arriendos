from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from main.services import (editar_user_sin_password, cambio_password, crear_user, crear_inmueble,
                        editar_inmueble, eliminar_inmueble, buscar_propiedad, save_image, filtro_comuna_region)
from django.contrib.auth.decorators import user_passes_test
from main.models import Inmueble, Region, Comuna, Imagen, UserProfile
from main.decorators import solo_propietario_staff, solo_arrendadores, solo_no_autentificado

# Create your views here.
def index(request):
    hay_busqueda = False
    propiedades = Inmueble.objects.all()
    datos = request.GET
    busqueda = datos.get('busqueda', '')
    comuna_cod = datos.get('comuna_cod', '')
    region_cod = datos.get('region_cod', '')
    tipo_inmueble = datos.get('tipo_inmueble', '')
    print(comuna_cod, region_cod)
    if busqueda:
        propiedades = buscar_propiedad(busqueda)
    else:
        propiedades = filtro_comuna_region(comuna_cod, region_cod, tipo_inmueble)
    comunas = Comuna.objects.all().order_by('nombre')
    regiones = Region.objects.all()
    if busqueda or comuna_cod or region_cod or tipo_inmueble:
        hay_busqueda = True
    context = {
        'comuna_cod_select': comuna_cod,
        'region_cod_select': region_cod,
        'tipos_inmuebles': Inmueble.inmuebles,
        'propiedades': propiedades,
        'comunas': comunas,
        'regiones': regiones,
        'hay_busqueda': hay_busqueda
    }
    return render(request, 'index.html', context)

@login_required
def profile(request):
    # Asegurar que el UserProfile esté creado
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    propiedades = Inmueble.objects.filter(propietario_id=user.id)
    context = {
        'propiedades': propiedades
    }

    if request.method == 'POST':
        if request.POST['telefono'].strip() != '':
            username = request.user
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            telefono = request.POST.get('telefono')
            rol = request.POST.get('rol')
            
            # Actualizar el UserProfile
            user_profile.telefono_personal = telefono
            user_profile.rol = rol
            user_profile.save()
            
            # Actualizar el User
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('profile')
        else:
            messages.error(request, 'El teléfono no puede estar vacío')

    return render(request, 'profile.html', context)

def change_pass(request):
    password = request.POST['password']
    password_repeat = request.POST['password_repeat']
    cambio_password(request, password, password_repeat)
    return redirect('/accounts/profile')

@user_passes_test(solo_no_autentificado)
def register(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            rol = request.POST['rol']
            password = request.POST['password']
            password_repeat = request.POST['password_repeat']

            # Ajustar la llamada a `crear_user` para incluir los nuevos argumentos
            crear_user(username, first_name, last_name, email, password, password_repeat, direccion, rol, telefono)
            
            messages.success(request, 'Usuario registrado exitosamente')
            return redirect('/accounts/login')
        
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, 'registration/register.html')

@login_required
@user_passes_test(solo_arrendadores)
def add_propiedad(request):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all().order_by('nombre')
    context = {
        'tipos_inmuebles': Inmueble.inmuebles,
        'regiones': regiones,
        'comunas': comunas,
    }
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        m2_construidos = int(request.POST['m2_construidos'])
        m2_totales = int(request.POST['m2_totales'])
        num_estacionamientos = int(request.POST['num_estacionamientos'])
        num_habitaciones = int(request.POST['num_habitaciones'])
        num_baños = int(request.POST['num_baños'])
        direccion = request.POST['direccion']
        precio_mensual_arriendo = int(request.POST['precio_mensual_arriendo'])
        tipo_de_inmueble = request.POST['tipo_de_inmueble']
        comuna_cod = request.POST['comuna_cod']
        rut_propietario = request.user
        
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
            imagen = save_image(imagen)
        else:
            imagen = None
        
        crear = crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, precio_mensual_arriendo, tipo_de_inmueble, comuna_cod, rut_propietario, imagen)
        if crear:
            messages.success(request, 'Propiedad ingresada con éxito')
            return redirect('profile')
        messages.error(request, 'Hubo un problema al crear la propiedad, favor revisar')
        return render(request, 'add_propiedad.html', context)
    else:
        return render(request, 'add_propiedad.html', context)

@login_required
def details_propiedad(request, id):
    id_buscado  = int(id)
    propiedad_encontrada = Inmueble.objects.get(id=id_buscado)
    context = {
        'propiedad': propiedad_encontrada
    }
    return render(request, 'detalles_propiedad.html', context)

@user_passes_test(solo_arrendadores)
@solo_propietario_staff
def edit_propiedad(request, id):
    inmueble = get_object_or_404(Inmueble, id=id)
    if request.method == 'GET':
        regiones = Region.objects.all()
        comunas = Comuna.objects.all().order_by('nombre')
        cod_region_actual = inmueble.comuna_id[:2]
        context = {
            'inmueble': inmueble,
            'regiones': regiones,
            'comunas': comunas,
            'cod_region': cod_region_actual
        }
        return render(request, 'edit_propiedad.html', context)

    # POST request: Procesar el formulario
    try:
        with transaction.atomic():
            # Extraer datos del formulario
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            m2_construidos = int(request.POST.get('m2_construidos'))
            m2_totales = int(request.POST.get('m2_totales'))
            num_estacionamientos = int(request.POST.get('num_estacionamientos'))
            num_habitaciones = int(request.POST.get('num_habitaciones'))
            num_baños = int(request.POST.get('num_baños'))
            direccion = request.POST.get('direccion')
            precio_mensual_arriendo = int(request.POST.get('precio_mensual_arriendo'))
            tipo_de_inmueble = request.POST.get('tipo_de_inmueble')
            comuna = request.POST.get('comuna_cod')
            rut_propietario = request.user

            # Procesar imagen si se envió una nueva
            imagen = save_image(request.FILES['imagen']) if 'imagen' in request.FILES else None

            # Editar inmueble usando el servicio
            editar = editar_inmueble(
                inmueble_id=inmueble.id,
                nombre=nombre,
                descripcion=descripcion,
                m2_construidos=m2_construidos,
                m2_totales=m2_totales,
                num_estacionamientos=num_estacionamientos,
                num_habitaciones=num_habitaciones,
                num_baños=num_baños,
                direccion=direccion,
                precio_mensual_arriendo=precio_mensual_arriendo,
                tipo_de_inmueble=tipo_de_inmueble,
                comuna=comuna,
                rut_propietario=rut_propietario,
                imagen=imagen
            )

            if editar:
                messages.success(request, 'Propiedad editada exitosamente')
                return redirect('profile')

    except Exception as e:
        messages.error(request, f'Error al editar la propiedad: {str(e)}')

    # Si hay un error, volver a mostrar el formulario con los datos actuales
    regiones = Region.objects.all()
    comunas = Comuna.objects.all().order_by('nombre')
    context = {
        'inmueble': inmueble,
        'regiones': regiones,
        'comunas': comunas,
        'cod_region': inmueble.comuna_id[:2]
    }
    return render(request, 'edit_propiedad.html', context)

@user_passes_test(solo_arrendadores)
@solo_propietario_staff
def delete_propiedad(request, id):
    inmueble = get_object_or_404(Inmueble, id=id)
    try:
        eliminar = eliminar_inmueble(id)
        if eliminar:
            messages.success(request, f'La propiedad {inmueble.nombre} fue eliminada')
        else:
            messages.error(request, 'Hubo un problema al eliminar la propiedad, favor revisar')
    except Exception as e:
        messages.error(request, f'Error al eliminar la propiedad: {str(e)}')

    return redirect('profile')
