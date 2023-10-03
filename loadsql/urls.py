from django.urls import path, include
from .views import *


urlpatterns = [
    path('', Loadsqls, name='loadsql'),
    path('upload/', upload_file, name='upload_file'),
]