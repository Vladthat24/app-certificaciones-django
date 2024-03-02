from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.generic.views.resolucion import ResolucionList, ResolucionCreate, ResolucionUpdate

app_name = 'resolucion'

urlpatterns = [
    path('list', login_required(ResolucionList.as_view()), name='list'),
    path('new,', login_required(ResolucionCreate.as_view()), name='new'),
    path('edit/<pk>', login_required(ResolucionUpdate.as_view()), name='edit'),

]
