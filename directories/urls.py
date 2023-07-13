from django.urls import path
from .views import *

urlpatterns = [
    path('os/', Os, name='os'),
    path('tmc/', Tmc, name='tmc'),
    path('upload-data/', upload_data, name='upload_data'),
    path('os_list/', OsList.as_view(), name='os_list'),
]
