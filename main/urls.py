from django.urls import path
from main.views import index, profile, edit_user

urlpatterns = [
    path('', index, name='index'),
    path('accounts/profile/', profile, name='profile',),
    path('edit-user/', edit_user, name='edit_user',),
]