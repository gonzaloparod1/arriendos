import csv
from django.core.management.base import BaseCommand
from main.services import crear_user

class Command(BaseCommand):
    help = 'Carga usuarios desde un archivo CSV'

    def handle(self, *args, **kwargs):
        with open('data/users.csv', 'r') as archivo:
            reader = csv.reader(archivo, delimiter=';')
            next(reader)  # Se salta la primera línea (cabeceras)

            for fila in reader:
                try:
                    crear_user(
                        username=fila[0],
                        first_name=fila[1],
                        last_name=fila[2],
                        email=fila[3],
                        password=fila[4],
                        password_confirm=fila[5],
                        direccion=fila[6],
                        rol=fila[7],
                        telefono=[8],
                    )
                    self.stdout.write(self.style.SUCCESS(f'Usuario {fila[1]} {fila[2]} creado correctamente'))
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(f'Advertencia: {e} - Usuario {fila[1]} {fila[2]} ya existe, ignorando.'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al crear usuario {fila[1]} {fila[2]}: {e}'))
