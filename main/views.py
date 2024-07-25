from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from main.services import editar_user_sin_password, cambio_password, crear_user, crear_inmueble, editar_inmueble, eliminar_inmueble, buscar_propiedad, save_image, filtro_comuna_region
from django.contrib.auth.decorators import user_passes_test
from main.models import Inmueble, Region, Comuna, Imagen
from main.decorators import solo_propietario_staff, solo_arrendadores, solo_no_autentificado

# Create your views here.
def index(request):
    propiedades = Inmueble.objects.all()
    datos = request.GET
    busqueda = datos.get('busqueda', '')
    comuna_cod = datos.get('comuna_cod', '')
    region_cod = datos.get('region_cod', '')
    print(comuna_cod, region_cod)
    if busqueda:
        propiedades = buscar_propiedad(busqueda)
    else:
        propiedades = filtro_comuna_region(comuna_cod, region_cod)
    comunas = Comuna.objects.all().order_by('nombre')
    regiones = Region.objects.all()
    context = {
        'propiedades': propiedades,
        'comunas': comunas,
        'regiones': regiones,
    }
    return render(request, 'index.html', context)

@login_required
def profile(request):
    id_usuario = request.user.id
    propiedades = Inmueble.objects.filter(propietario_id=id_usuario)
    context = {
        'propiedades': propiedades
    }

    if request.method == 'POST':
        if request.POST['telefono'].strip() != '':
            username = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            direccion = request.POST['direccion']
            telefono = request.POST['telefono']
            rol = request.POST['rol']
            editar_user_sin_password(username, first_name, last_name, email, direccion, rol, telefono)
            messages.success(request, 'Ha actualizado sus datos con exito')
            return redirect('/accounts/profile')
        else:
            username = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            direccion = request.POST['direccion']
            rol = request.POST['rol']
            
            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                imagen = save_image(imagen)
            else:
                imagen = None
            
            editar_user_sin_password(username, first_name, last_name, email, rol, direccion, imagen)
            messages.success(request, 'Ha actualizado sus datos con exito sin telefono')
            return redirect('/accounts/profile')
    else:
        return render(request, 'profile.html', context)

def change_pass(request):
    password = request.POST['password']
    password_repeat = request.POST['password_repeat']
    cambio_password(request, password, password_repeat)
    return redirect('/accounts/profile')

@user_passes_test(solo_no_autentificado)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        rol = request.POST['rol']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']
        crear = crear_user(request, username, first_name, last_name, email, password, password_repeat, direccion, rol, telefono)
        if crear:
            return redirect('/accounts/login')
        # Si hay errores, mantiene los datos ingresados en el formulario
        return render(request, 'registration/register.html', {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'direccion': direccion,
            'telefono': telefono,
            'rol': rol,
        })
    else:
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
    id  = int(id)
    propiedad_encontrada = None
    propiedades = Inmueble.objects.all()
    for propiedad in propiedades:
        if propiedad.id == id:
            propiedad_encontrada = propiedad
            break
    context = {
        'propiedad': propiedad_encontrada
    }
    return render(request, 'detalles_propiedad.html', context)

@user_passes_test(solo_arrendadores)
@solo_propietario_staff
def edit_propiedad(request, id):
    if request.method == 'GET':
        inmueble = Inmueble.objects.get(id=id)
        regiones = Region.objects.all()
        comunas = Comuna.objects.all().order_by('nombre')
        cod_region_actual = inmueble.comuna_id[0:2]
        context = {
            'inmueble': inmueble,
            'regiones': regiones,
            'comunas': comunas,
            'cod_region': cod_region_actual
        } 
        return render(request, 'edit_propiedad.html', context)
    else:
        inmueble_id = id
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
        comuna = request.POST['comuna_cod']
        rut_propietario = request.user
        
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
            imagen = save_image(imagen)
        else:
            imagen = None
        
        editar = editar_inmueble(inmueble_id, nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, precio_mensual_arriendo, tipo_de_inmueble, comuna, rut_propietario, imagen)
        if editar:
            messages.success(request, 'Propiedad editada exitosamente')
            return redirect('profile')
        messages.error(request, 'Hubo un problema al editar la propiedad, favor revisar')
        return render(request, 'edit_propiedad.html', context)

@user_passes_test(solo_arrendadores)
@solo_propietario_staff
def delete_propiedad(request, id):
    eliminar = eliminar_inmueble(id)
    if eliminar:
        messages.error(request, f'La propiedad {id} fue eliminada')
        return redirect('profile')
    else:
        messages.error(request, 'Hubo un problema al eliminar la propiedad, favor revisar')
        return render(request, 'profile.html', context)
