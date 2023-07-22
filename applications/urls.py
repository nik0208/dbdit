from django.urls import path
from .views import *


urlpatterns = [
    path('', Application, name='applications'),
    path('applications_list/', ApplicationsList.as_view(), name='applications_list'),
]
