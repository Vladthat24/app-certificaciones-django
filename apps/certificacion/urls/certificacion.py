from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.certificacion.views.certificacion import CertificacionCreateModalView, CertificacionUpdateModalView, \
    CertificacionList, CertificacionCreateView, CertificacionUpdateView, CertificacionDelete, \
    Certificacion2UpdateModalView
from apps.certificacion.views.report_pdf_certificacion import print_certificado_pdf
from apps.certificacion.views.report_pdf_certificacion_no_covid import print_certificado_no_covid_pdf

app_name = 'certificacion'

urlpatterns = [
    path('<solicitud_pk>/new', login_required(CertificacionCreateModalView.as_view()), name='new'),
    path('<solicitud_pk>/edit/<pk>', login_required(CertificacionUpdateModalView.as_view()), name='edit'),
    path('list', login_required(CertificacionList.as_view()), name='list'),
    path('report/<pk>', login_required(print_certificado_pdf), name='report'),
    path('new', login_required(CertificacionCreateView.as_view()), name='new'),
    path('edit/<pk>', login_required(CertificacionUpdateView.as_view()), name='edit'),
    path('delete/<pk>', login_required(CertificacionDelete.as_view()), name='delete'),
    path('edit2/<solicitud_pk>', login_required(Certificacion2UpdateModalView.as_view()), name='edit2'),
    path('report-no-covid/<pk>', login_required(print_certificado_no_covid_pdf), name='report-no-covid'),
]
