from django.contrib.auth.decorators import login_required
from django.urls import path

from setup.views.entidad import EntidadList, EntidadCreate, EntidadUpdate

app_name = 'entidad'

urlpatterns = [
    path('list', login_required(EntidadList.as_view()), name='list'),
    path('new,', login_required(EntidadCreate.as_view()), name='new'),
    path('edit/<pk>', login_required(EntidadUpdate.as_view()), name='edit'),

]
