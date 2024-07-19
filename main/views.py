from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from main.services import editar_user_sin_password, cambio_password, crear_user

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
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
            editar_user_sin_password(username, first_name, last_name, email, rol, direccion)
            messages.success(request, 'Ha actualizado sus datos con exito sin telefono')
            return redirect('/accounts/profile')
    else:
        return render(request, 'profile.html')

def change_pass(request):
    password = request.POST['password']
    password_repeat = request.POST['password_repeat']
    cambio_password(request, password, password_repeat)
    return redirect('/accounts/profile')

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