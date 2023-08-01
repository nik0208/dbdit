from django.urls import path
from .views import *

urlpatterns = [
    path('os/', Os, name='os'),
    path('tmc/', Tmc, name='tmc'),
    path('upload-data-os/', upload_data_os, name='upload_data_os'),
    path('upload-data-tmc/', upload_data_tmc, name='upload_data_tmc'),
    path('os_list/', OsList.as_view(), name='os_list'),
    path('tmc_list/', TmcList.as_view(), name='tmc_list'),
    path('load_to_sdp/', load_to_sdp, name='load_to_sdp')
]
