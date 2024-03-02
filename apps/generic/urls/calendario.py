from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.generic.views.calendario import calendar_view, lista_calendario, actualizar_calendario

app_name = 'calendario'

urlpatterns = [
    path('show', login_required(calendar_view), name='show'),
    path('list', login_required(lista_calendario), name='list'),
    path('update', login_required(actualizar_calendario), name='update')

]
