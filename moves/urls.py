from django.urls import path
from .views import *

urlpatterns = [

    path('', Moves, name='moves'),
    path('addtmcmove/', AddTmcMove, name='addtmcmove'),
    path('addmove/', AddMove, name='addmove'),
    path('generatemovedocument/<int:move_id>', GenerateMoveDocument,
         name='generate_move_document')

]
