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
    path('generate_act_document/<int:act_id>', GenerateActDocument,
         name='generate_act_document'),
    path('get_acts/', get_acts, name='get_acts'),
    path('create_based_on_act/<int:act_id>',
         CreateBasedOnAct, name='create_based_on_act'),
    path('upload-data-acts/', upload_data_acts, name='upload_data_acts'),
    path('add_os/', add_os, name='add_os'),
    path('select2/', include('django_select2.urls', namespace='django_select2')),

]
