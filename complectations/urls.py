from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Complectations,  name='complectations'),
    path('add_complectations/', AddComplectations, name='add_complectations'),

]

