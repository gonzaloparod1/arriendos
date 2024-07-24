from django.urls import path
from main.views import index, profile, change_pass, register, add_propiedad, details_propiedad, edit_propiedad, delete_propiedad

urlpatterns = [
    path('', index, name='index'),
    path('accounts/profile/', profile, name='profile',),
    path('accounts/change-pass/', change_pass, name='change_pass',),
    path('accounts/register/', register, name='register',),
    path('propiedad/add-propiedad/', add_propiedad, name='add_propiedad',),
    path('propiedad/detalles/<id>', details_propiedad, name='details_propiedad',),
    path('propiedad/edit-propiedad/<id>', edit_propiedad, name='edit_propiedad',),
    path('propiedad/delete-propiedad/<id>', delete_propiedad, name='delete_propiedad',),
]