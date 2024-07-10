from main.models import UserProfile
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

def crear_inmueble(*args):
    pass

def editar_inmueble(*args):
    pass

def eliminar_inmueble(inmueble_id):
    pass

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