from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Acts, name='acts'),
    path('addact/', AddAct, name='add_act'),
    path('actedit/<int:act_id>', ActEdit, name='act_edit'),
    path('actdelete/<int:act_id>', ActDelete, name='act_delete'),
    path('acts/<int:act_id>/generate_document/', GenerateActDocument,
         name='generate_act_document'),
    path('get_acts/', get_acts, name='get_acts'),
    path('create_based_on_act/<int:act_id>',
         CreateBasedOnAct, name='create_based_on_act'),
    path('select2/', include('django_select2.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
