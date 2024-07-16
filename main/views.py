from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from main.services import editar_user_sin_password

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_user(request):
    username = request.user
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    direccion = request.POST['direccion']
    telefono = request.POST['telefono']
    editar_user_sin_password(username, first_name, last_name, email, direccion, telefono)
    return HttpResponse('Datos actualizados')