from django.urls import path
from .views import *

urlpatterns = [

    path('', Moves, name='moves'),
    path('moves_list/', MovesList.as_view(), name='moves_list'),
    path('add_move/', AddMove, name='add_move'),
    path('generatemovedocument/<int:move_id>', GenerateMoveDocument,
         name='generate_move_document')
]
