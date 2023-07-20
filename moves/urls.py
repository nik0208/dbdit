from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', Moves, name='moves'),
    path('moves_list/', MovesList.as_view(), name='moves_list'),
    path('add_move/', AddMove, name='add_move'),
    path('generatemovedocument/<int:move_id>', GenerateMoveDocument,
         name='generate_move_document'),
    path('select2/', include('django_select2.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
