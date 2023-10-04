from django.urls import path
from .views import *

urlpatterns = [
    path('os/', Os, name='os'),
    path('tmc/', Tmc, name='tmc'),
    path('os_list/', OsList.as_view(), name='os_list'),
    path('tmc_list/', TmcList.as_view(), name='tmc_list'),
    
]
