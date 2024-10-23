import csv
import os
from django.core.management.base import BaseCommand
from main.services import crear_inmueble
from django.core.files import File

class Command(BaseCommand):
    help = 'Carga inmuebles desde un archivo CSV'

    def handle(self, *args, **kwargs):
        media_dir = 'media/inmuebles/'  # Asegúrate de que las imágenes estén en este directorio
        with open('data/inmuebles.csv', 'r') as archivo:
            reader = csv.reader(archivo, delimiter=',')
            next(reader)  # Se salta la primera línea (cabeceras)

            for fila in reader:
                try:
                    # Construir la ruta de la imagen
                    imagen_path = os.path.join(media_dir, f"{fila[0].replace(' ', '_').lower()}.jpg")
                    
                    # Verifica si la imagen existe
                    if os.path.exists(imagen_path):
                        with open(imagen_path, 'rb') as img_file:
                            imagen = File(img_file)
                            crear_inmueble(
                                fila[0], fila[1], fila[2], fila[3], fila[4], fila[5],
                                fila[6], fila[7], fila[8], fila[9], fila[10], fila[11], imagen
                            )
                            self.stdout.write(self.style.SUCCESS(f'Inmueble {fila[0]} creado correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Imagen para {fila[0]} no encontrada.'))
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al crear inmueble {fila[0]}: {e}'))
