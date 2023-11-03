from django.urls import path, include
from .views import *


urlpatterns = [
    path('', Loadsqls, name='loadsql'),
    path('upload/', upload_file, name='upload_file'),
    # path('add_act_skans/', add_act_skans, name='add_act_skans'),
]
