from main.models import UserProfile, User

def crear_inmueble(*args):
    pass

def editar_inmueble(*args):
    pass

def eliminar_inmueble(inmueble_id):
    pass

def crear_user(rut:str, first_name:str, last_name:str, email:str, password:str, direccion:str, telefono:str):
    user = User.objects.create_user(
        username=rut,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    UserProfile.objects.create(
        direccion=direccion,
        telefono_personal=telefono,
        user=user
    )

def editar_user(*args):
    pass

def eliminar_user(user_id):
    pass