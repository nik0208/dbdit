from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Acts, name='acts'),
    path('addact/', AddAct, name='add_act'),
    path('acts_list/', ActsList.as_view(), name='acts_list'),
    path('act_edit/<int:act_id>', ActEdit, name='act_edit'),
    path('act_delete/<int:act_id>', ActDelete, name='act_delete'),
    path('acts/<int:act_id>/generate_document/', GenerateActDocument,
         name='generate_act_document'),
    path('get_acts/', get_acts, name='get_acts'),
    path('create_based_on_act/<int:act_id>',
         CreateBasedOnAct, name='create_based_on_act'),

]

