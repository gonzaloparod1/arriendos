from django.db import connection

# class Command(BaseCommand):
#    def handle(self, *args, **kwargs):
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT *
#                 FROM main_comuna
#                 WHERE cod='05804'
#             """)
#             resultados = cursor.fetchall() # Lista de tuplas. Cada tupla representa una fila de la tabla y contiene los valores de las columnas correspondientes
#             print(resultados) # [('05804', 'Villa Alemana', '05')]


# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         for comuna in Comuna.objects.raw("""
#                 SELECT cod, nombre, region_id
#                 FROM main_comuna
#                 WHERE cod='05804'
#             """):
#             print(comuna.cod)
#             print(comuna.nombre)
#             print(comuna.region_id)