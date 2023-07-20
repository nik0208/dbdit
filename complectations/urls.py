from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path ('', Complectations,  name='complectations'),
    path ('add_complectations/', AddComplectations, name='add_complectations' ),
    path('select2/', include('django_select2.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)