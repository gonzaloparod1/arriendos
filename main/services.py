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

def editar_user(*args):
    pass

def eliminar_user(rut:str):
    eliminar = User.objects.get(username=rut)
    eliminar.delete()