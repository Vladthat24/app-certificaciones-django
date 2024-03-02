from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.solicitud.views.estado_observado import ListaEstadosSolicitud
from apps.solicitud.views.person_api import get_persona_by_dni_reniec
from apps.solicitud.views.report_pdf_solicitud import print_solicitud_pdf
from apps.solicitud.views.solicitud import SolicitudList, SolicitudCreate, SolicitudUpdate, SolicitudDelete, \
    save_nro_expediente, aprobar_solicitud_tesoreria, \
    guardar_escaneado, eliminar_escaneado, observar_solicitud, levantar_observacion_solicitud, SolicitudDetailView

app_name = 'solicitud'

urlpatterns = [

    path('list', login_required(SolicitudList.as_view()), name='list'),

    path('list-observadas', login_required(SolicitudList.as_view()), name='list-observadas'),

    path('new', login_required(SolicitudCreate.as_view()), name='new'),

    path('edit/<pk>', login_required(SolicitudUpdate.as_view()), name='edit'),

    path('validar-persona/<dni>', login_required(get_persona_by_dni_reniec), name='validar-persona'),

    path('report/<pk>', login_required(print_solicitud_pdf), name='report'),

    path('delete/<pk>', login_required(SolicitudDelete.as_view()), name='delete'),

    path('list-tesoreria-validadas', login_required(SolicitudList.as_view()),
         name='list-tesoreria-validadas'),

    path('aprobar-solicitud-tesoreria', login_required(aprobar_solicitud_tesoreria),
         name='aprobar-solicitud-tesoreria'),

    path('save-nro-expediente', login_required(save_nro_expediente), name='save-nro-expediente'),

    path('detail/<pk>', login_required(SolicitudDetailView.as_view()), name='detail'),

    path('guardar-escaneado', login_required(guardar_escaneado), name='guardar-escaneado'),

    path('eliminar-escaneado', login_required(eliminar_escaneado), name='eliminar-escaneado'),

    path('levantar-observacion', login_required(levantar_observacion_solicitud), name='levantar-observacion'),

    path('lista-estados-solicitud', login_required(ListaEstadosSolicitud.as_view()), name='lista-estados-solicitud'),

    path('observar', login_required(observar_solicitud), name='observar'),

]
