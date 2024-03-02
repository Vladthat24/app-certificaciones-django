import datetime
from io import BytesIO

import pandas as pd
from django.http import HttpResponse
from django.template import loader

from apps.certificacion.models.certificacion import Certificacion
from apps.solicitud.models.solicitud import Solicitud, LUGAR_FALLECIMIENTO
from apps.util.update_menu import update_menu


def generate_excel_observaciones_get_form(request):
    update_menu(request)

    context = {
        'title': 'GENERAR EXCEL OBSERVACIONES'
    }

    template = loader.get_template('reporte_excel/reporte_excel_observaciones.html')

    if request.method == 'POST':
        template = loader.get_template('reporte_excel/reporte_excel_observaciones_detalle.html')

        fecha_inicio = request.POST.get('fecha_inicio', '12/12/12')
        fecha_final = request.POST.get('fecha_final', '12/12/12')
        tipo = request.POST.get('tipo', '1')
        fecha_inicio_ = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_final_ = datetime.datetime.strptime(fecha_final, '%Y-%m-%d')

        # ->>  Solicitud example
        # solicitud = Solicitud.objects.get(pk=25)
        # solicitud.estados.all()

        queryset = Solicitud.objects.filter(registrado_fecha__range=[fecha_inicio_, fecha_final_],
                                            estados__isnull=False)

        if tipo == "2":
            queryset = queryset.filter(solicitud__es_covid=True)

        if tipo == "3":
            queryset = queryset.filter(solicitud__es_covid=False)

        count = queryset.count()

        context['object_list'] = queryset
        context['count'] = count
        context['fecha_inicio'] = fecha_inicio
        context['fecha_final'] = fecha_final
        context['tipo'] = tipo

    return HttpResponse(template.render(context, request))


def generate_excel_observaciones_file(request):
    if request.method == 'GET':

        columnas_title_excel = []
        # columnas_excel = {}

        fecha_inicio = request.GET.get('fecha_inicio', '12/12/12')
        fecha_final = request.GET.get('fecha_final', '12/12/12')
        tipo = request.POST.get('tipo', '1')

        fecha_inicio_ = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_final_ = datetime.datetime.strptime(fecha_final, '%Y-%m-%d')

        queryset = Solicitud.objects.filter(registrado_fecha__range=[fecha_inicio_, fecha_final_],
                                            estados__isnull=False)
        if tipo == "2":
            queryset = queryset.filter(es_covid=True)

        if tipo == "3":
            queryset = queryset.filter(es_covid=False)

        queryset.distinct().order_by('-created_at')

        columnas_title_excel.append('ES COVID')
        columnas_title_excel.append('N° DE AUTORIZACIÓN')
        columnas_title_excel.append('N° EXP')
        columnas_title_excel.append('FECHA INGRESO DE EXPEDIENTE')
        columnas_title_excel.append('SOLICITANTE')
        columnas_title_excel.append('N° DNI')
        columnas_title_excel.append('PARENTESCO CON EL SOLICITANTE')
        columnas_title_excel.append('PARENTESCO CON EL FALLECIDO')
        columnas_title_excel.append('NOMBRE DEL FALLECIDO')
        columnas_title_excel.append('DNI DEL FALLECIDO')
        columnas_title_excel.append('FECHA FALLECIMIENTO')
        columnas_title_excel.append('HORA DE FALLECIMIENTO')
        columnas_title_excel.append('DIRECCIÓN DE FALLECIMIENTO TIPO')
        columnas_title_excel.append('DIRECCIÓN DE FALLECIMIENTO')
        columnas_title_excel.append('CAUSA  DE MUERTE SEGÚN NECROPSIA')
        columnas_title_excel.append('DIAGNÓSTICO CLÍNICO')
        columnas_title_excel.append('N° CERTIF Y PROT. DE NECROPSIA')
        columnas_title_excel.append('FECHA CERT. NECROPSIA')
        columnas_title_excel.append('EMPRESA (CREMATORIO)')
        columnas_title_excel.append('FECHA DE CREMACIÓN')
        columnas_title_excel.append('OBSERVACIONES')

        df = pd.DataFrame(columns=columnas_title_excel)

        for solicitud in queryset:
            certificacion = None
            try:
                certificacion = solicitud.certificacion
            except  Certificacion.DoesNotExist as e:
                print(e)

            contenido = {
                "ES COVID": "SI" if solicitud.es_covid else "NO",
                "N° DE AUTORIZACIÓN": certificacion.numero_autorizacion if certificacion else "-",
                "N° EXP": solicitud.numero_expediente if solicitud.numero_expediente else "-",
                "FECHA INGRESO DE EXPEDIENTE": solicitud.registrado_fecha.strftime(
                    "%d/%m/%Y") if solicitud.registrado_fecha else "-",
                "SOLICITANTE": solicitud.get_solicitante(),
                "N° DNI": solicitud.solicitante_numero_documento,
                "PARENTESCO CON EL SOLICITANTE": solicitud.get_solicitante_parentesco_display(),
                "PARENTESCO CON EL FALLECIDO": solicitud.get_fallecido_parentesco_display(),
                "NOMBRE DEL FALLECIDO": solicitud.get_fallecido(),
                "DNI DEL FALLECIDO": solicitud.fallecido_numero_documento,
                "FECHA FALLECIMIENTO": solicitud.fallecido_fecha_fallecimiento.strftime(
                    "%d/%m/%Y") if solicitud.fallecido_fecha_fallecimiento else "-",
                "HORA DE FALLECIMIENTO": solicitud.fallecido_hora_fallecimiento if solicitud.fallecido_hora_fallecimiento else "-",
                "DIRECCIÓN DE FALLECIMIENTO TIPO": dict(LUGAR_FALLECIMIENTO)[solicitud.lugar_fallecimiento_tipo],
                "DIRECCIÓN DE FALLECIMIENTO": certificacion.fallecido_direccion if certificacion else
                solicitud.get_direccion_fallecimiento()["direccion"],
                "CAUSA  DE MUERTE SEGÚN NECROPSIA": certificacion.necropsia_causa_muerte if certificacion else "",
                "DIAGNÓSTICO CLÍNICO": certificacion.motivo if certificacion else "",
                "N° CERTIF Y PROT. DE NECROPSIA": certificacion.necropsia_numero if certificacion else "",
                "FECHA CERT. NECROPSIA": certificacion.fecha_cert_necropsia if certificacion else "",
                "EMPRESA (CREMATORIO)": solicitud.crematorio.nombre,
                "FECHA DE CREMACIÓN": solicitud.fecha_cremacion,

            }
            observaciones = ""
            if len(solicitud.estados.all()) > 1:
                observaciones = "(1) -----------------------------\n"

            for index, obs in enumerate(solicitud.estados.all()):
                observaciones = observaciones + " * USUARIO OBSERVACIÓN: " + str(obs.created_by) + "\n" + \
                                " * FECHA OBSERVACIÓN: " + str(obs.created_at) + "\n" + \
                                " * OBSERVACIÓN: " + str(obs.observacion) + "\n" + \
                                " * USUARIO DESCARGO: " + str(obs.updated_by) + "\n" + \
                                " * FECHA DESCARGO: " + str(obs.updated_at) + "\n" + \
                                " * DESCARGO: " + str(obs.descargo if obs.descargo else "--") + "\n"

                if index < len(solicitud.estados.all()) - 1:
                    observaciones = observaciones + "(" + str(index + 2) + ") -----------------------------\n"

            contenido["OBSERVACIONES"] = observaciones

            df = df.append(contenido, ignore_index=True)

        # df = pd.DataFrame(columnas_excel, columns=columnas_title_excel)
        df.index = df.index + 1

        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Página1')

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets['Página1']

            writer.save()
            filename = 'Trama-autorizaciones_' + fecha_inicio + "--" + fecha_final
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response


    else:
        return HttpResponse("Operación no soportada")
