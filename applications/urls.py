from django.urls import path
from .views import *


urlpatterns = [
    path('', Application, name='applications')
]
