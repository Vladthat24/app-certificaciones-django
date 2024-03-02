from django.urls import path

from apps.reporte_excel.views.reporte_excel import generate_excel_get_form, generate_excel_file
from apps.reporte_excel.views.reporte_excel_observaciones import generate_excel_observaciones_get_form, \
    generate_excel_observaciones_file

app_name = 'reporte-excel'

urlpatterns = [
    path('reporte-excel-form', generate_excel_get_form, name='reporte-excel-form'),
    path('generar-excel', generate_excel_file, name='generar-excel'),

    path('reporte-excel-observaciones-form', generate_excel_observaciones_get_form,
         name='reporte-excel-observaciones-form'),
    path('generar-excel-observaciones', generate_excel_observaciones_file, name='generar-excel-observaciones'),

]
