from django.contrib.auth.decorators import login_required
from django.urls import path

from setup.views.crematorio import CrematorioList, CrematorioCreate, CrematorioUpdate

app_name = 'crematorio'

urlpatterns = [
    path('list', login_required(CrematorioList.as_view()), name='list'),
    path('new,', login_required(CrematorioCreate.as_view()), name='new'),
    path('edit/<pk>', login_required(CrematorioUpdate.as_view()), name='edit'),

]
