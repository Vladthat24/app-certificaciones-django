import datetime
from io import BytesIO

import pandas as pd
from django.http import HttpResponse
from django.template import loader

from apps.certificacion.models.certificacion import Certificacion
from apps.solicitud.models.solicitud import LUGAR_FALLECIMIENTO
from apps.util.update_menu import update_menu


def generate_excel_get_form(request):
    update_menu(request)

    context = {
        'title': 'GENERAR EXCEL SOLICITUDES'
    }

    template = loader.get_template('reporte_excel/reporte_excel.html')
    if request.method == 'POST':
        template = loader.get_template('reporte_excel/reporte_excel_detalle.html')

        fecha_inicio = request.POST.get('fecha_inicio', '12/12/12')
        fecha_final = request.POST.get('fecha_final', '12/12/12')
        tipo = request.POST.get('tipo', '1')

        fecha_inicio_ = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_final_ = datetime.datetime.strptime(fecha_final, '%Y-%m-%d')

        queryset = Certificacion.objects.filter(solicitud__registrado_fecha__range=[fecha_inicio_, fecha_final_])

        if tipo == "2":
            queryset = queryset.filter(solicitud__es_covid=True)

        if tipo == "3":
            queryset = queryset.filter(solicitud__es_covid=False)

        count = queryset.count()

        context['object_list'] = queryset
        context['count'] = count
        context['fecha_inicio'] = fecha_inicio
        context['fecha_final'] = fecha_final

    return HttpResponse(template.render(context, request))


def generate_excel_file(request):
    if request.method == 'GET':

        columnas_title_excel = []
        columnas_excel = {}

        fecha_inicio = request.GET.get('fecha_inicio', '12/12/12')
        fecha_final = request.GET.get('fecha_final', '12/12/12')
        tipo = request.POST.get('tipo', '1')

        fecha_inicio_ = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_final_ = datetime.datetime.strptime(fecha_final, '%Y-%m-%d')

        object_list = Certificacion.objects.filter(solicitud__registrado_fecha__range=[fecha_inicio_, fecha_final_])

        if tipo == "2":
            object_list = object_list.filter(solicitud__es_covid=True)

        if tipo == "3":
            object_list = object_list.filter(solicitud__es_covid=False)

        columnas_title_excel.append('ES COVID')
        columnas_excel['ES COVID'] = ["SI" if i['solicitud__es_covid'] else "NO" for i in
                                      object_list.values('solicitud__es_covid')]

        columnas_title_excel.append('N° DE AUTORIZACIÓN')
        columnas_excel['N° DE AUTORIZACIÓN'] = [i['numero_autorizacion'] for i in
                                                object_list.values('numero_autorizacion')]

        columnas_title_excel.append('N° EXP')
        columnas_excel['N° EXP'] = [i['solicitud__numero_expediente'] for i in
                                    object_list.values('solicitud__numero_expediente')]

        # , % H: % M: % S
        columnas_title_excel.append('FECHA INGRESO DE EXPEDIENTE')
        columnas_excel['FECHA INGRESO DE EXPEDIENTE'] = [i['solicitud__registrado_fecha'].strftime("%d/%m/%Y") for i in
                                                         object_list.values('solicitud__registrado_fecha')]

        columnas_title_excel.append('SOLICITANTE')
        columnas_excel['SOLICITANTE'] = [i['solicitante'] for i in object_list.values('solicitante')]

        columnas_title_excel.append('N° DNI')
        columnas_excel['N° DNI'] = [i['solicitante_dni'] for i in object_list.values('solicitante_dni')]

        columnas_title_excel.append('PARENTESCO CON EL SOLICITANTE')
        columnas_excel['PARENTESCO CON EL SOLICITANTE'] = [i['parentesco_solicitante'] for i in
                                                           object_list.values('parentesco_solicitante')]

        columnas_title_excel.append('PARENTESCO CON EL FALLECIDO')
        columnas_excel['PARENTESCO CON EL FALLECIDO'] = [i['parentesco'] for i in object_list.values('parentesco')]

        columnas_title_excel.append('NOMBRE DEL FALLECIDO')
        columnas_excel['NOMBRE DEL FALLECIDO'] = [i['fallecido_nombre'] for i in object_list.values('fallecido_nombre')]

        columnas_title_excel.append('DNI DEL FALLECIDO')
        columnas_excel['DNI DEL FALLECIDO'] = [i['fallecido_dni'] for i in object_list.values('fallecido_dni')]

        columnas_title_excel.append('FECHA FALLEC')
        columnas_excel['FECHA FALLEC'] = [i['fallecido_fecha'] if i['fallecido_fecha'] else "" for i
                                          in object_list.values('fallecido_fecha')]

        columnas_title_excel.append('HORA DE FALLECIMIENTO')
        columnas_excel['HORA DE FALLECIMIENTO'] = [i['fallecido_hora'] for i in object_list.values('fallecido_hora')]

        columnas_title_excel.append('NÚMERO DE NECROPSIA')
        columnas_excel['NÚMERO DE NECROPSIA'] = [i['solicitud__numero_necropsia'] for i in
                                                 object_list.values('solicitud__numero_necropsia')]

        columnas_title_excel.append('FECHA DE NECROPSIA')
        columnas_excel['FECHA DE NECROPSIA'] = [ i['solicitud__fecha_necropsia'].strftime("%d/%m/%Y") if i['solicitud__fecha_necropsia'] else "-" for i in
                                                object_list.values('solicitud__fecha_necropsia')]

        columnas_title_excel.append('DIRECCIÓN DE FALLECIMIENTO TIPO')
        columnas_excel['DIRECCIÓN DE FALLECIMIENTO TIPO'] = [
            dict(LUGAR_FALLECIMIENTO)[int(i['solicitud__lugar_fallecimiento_tipo'])] for i in
            object_list.values('solicitud__lugar_fallecimiento_tipo')]

        columnas_title_excel.append('DIRECCIÓN DE FALLECIMIENTO')
        columnas_excel['DIRECCIÓN DE FALLECIMIENTO'] = [i['fallecido_direccion'] for i in
                                                        object_list.values('fallecido_direccion')]

        columnas_title_excel.append('CAUSA  DE MUERTE SEGÚN NECROPSIA')
        columnas_excel['CAUSA  DE MUERTE SEGÚN NECROPSIA'] = [i['necropsia_causa_muerte'] for i in
                                                              object_list.values('necropsia_causa_muerte')]

        columnas_title_excel.append('DIAGNÓSTICO CLÍNICO')
        columnas_excel['DIAGNÓSTICO CLÍNICO'] = [i['motivo'] for i in object_list.values('motivo')]

        columnas_title_excel.append('N° CERTIF Y PROT. DE NECROPSIA')
        columnas_excel['N° CERTIF Y PROT. DE NECROPSIA'] = [i['necropsia_numero'] for i in
                                                            object_list.values('necropsia_numero')]

        columnas_title_excel.append('FECHA CERT. NECROPSIA')
        columnas_excel['FECHA CERT. NECROPSIA'] = [i['fecha_cert_necropsia'] if
                                                   i['fecha_cert_necropsia'] else "" for i in
                                                   object_list.values('fecha_cert_necropsia')]

        columnas_title_excel.append('EMPRESA (CREMATORIO)')
        columnas_excel['EMPRESA (CREMATORIO)'] = [i['solicitud__crematorio__nombre'] for i in
                                                  object_list.values('solicitud__crematorio__nombre')]

        columnas_title_excel.append('FECHA DE CREMACIÓN')
        columnas_excel['FECHA DE CREMACIÓN'] = [i['solicitud__fecha_cremacion'] for i in
                                                object_list.values('solicitud__fecha_cremacion')]

        # columnas_excel = {}
        #
        # columnas_title_excel.append('N°')
        # columnas_excel['N°'] = ['1', '2', '3', '4']

        df = pd.DataFrame(columnas_excel, columns=columnas_title_excel)
        df.index = df.index + 1

        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Página1')

            for column in df:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Página1'].set_column(col_idx + 1, col_idx + 1, column_length)

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets['Página1']
            # format1 = workbook.add_format({'num_format': ''})
            # worksheet.set_column(1, 61, 20, format1)

            writer.save()
            filename = 'Trama-autorizaciones_' + fecha_inicio + "--" + fecha_final
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response


    else:
        return HttpResponse("Operación no soportada")
