from django.urls import path
from .views import *

urlpatterns = [

    path('', Moves, name='moves'),
    path('addtmcmove/', AddTmcMove, name='addtmcmove'),
    path('addosmove/', AddOsMove, name='addosmove'),
    path('generatemovedocument/<int:move_id>', GenerateMoveDocument,
         name='generate_move_document')

]
