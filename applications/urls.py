from django.urls import path
from .views import *


urlpatterns = [
    path('', Application, name='applications'),
    path('applications_list/', ApplicationsList.as_view(), name='applications_list'),
    path('upload-data/', upload_data_appl, name='upload_data'),
    path('addappl/', AddAppl, name='add_appl'),
    path('updstatus/<int:pk>/', UpdateStatus, name='updstatus'),
    
]
