from django.urls import path
from main.views import index, profile, change_pass

urlpatterns = [
    path('', index, name='index'),
    path('accounts/profile/', profile, name='profile',),
    path('accounts/change-pass/', change_pass, name='change_pass',),
]