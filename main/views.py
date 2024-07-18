from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from main.services import editar_user_sin_password

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
            editar_user_sin_password(username, first_name, last_name, email, direccion, telefono)
            messages.success(request, 'Ha actualizado sus datos con exito')
            return redirect('/accounts/profile')
        else:
            username = request.user
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            direccion = request.POST['direccion']
            editar_user_sin_password(username, first_name, last_name, email, direccion)
            messages.success(request, 'Ha actualizado sus datos con exito sin telefono')
            return redirect('/accounts/profile')
    else:
        return render(request, 'profile.html')