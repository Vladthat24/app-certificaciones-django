from django.urls import path

from apps.reporte_grafico.views.solicitud import grafico_get_form

app_name = 'reporte-grafico'

urlpatterns = [
    path('solicitud-form', grafico_get_form, name='solicitud-form'),
    # path('generar-excel', generate_excel_file, name='generar-excel'),
]
