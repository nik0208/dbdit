from django.urls import path
from .views import *


urlpatterns = [
    path ('', Complectations,  name='complectations'),
    path ('add_complectations/', AddComplectations, name='add_complectations' )
]
