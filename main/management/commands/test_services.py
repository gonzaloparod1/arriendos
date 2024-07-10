from django.core.management.base import BaseCommand
from main.services import *

# Se ejecuta usando python manage.py test_client

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        #crear_user('44.444.444-4', 'Cuatro', 'Jor', 'ccc@bbb.ccc', '123456', '123456', 'Pasaje Nueve, Chile')
        editar_user('44.444.444-4', 'Cuatro', 'Jordan', 'ccc@bbb.ccc', '654321', '654321', 'Street One, Usa', '987654321')
