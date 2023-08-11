from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', Moves, name='moves'),
    path('moves_list/', MovesList.as_view(), name='moves_list'),
    path('add_move_os/', AddMoveOS, name='add_move_os'),
    path('add_move_tmc/', AddMoveTmc, name='add_move_tmc'),
    path('generatemovedocument/<int:move_id>', GenerateMoveDocument,
         name='generate_move_document'),
    path('move_details/<int:move_pk>', get_move_details, name='move_details'),

]

