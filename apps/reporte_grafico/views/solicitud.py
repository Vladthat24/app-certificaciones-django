import datetime

from django.http import HttpResponse
from django.template import loader

from apps.solicitud.models.solicitud import Solicitud
from apps.util.update_menu import update_menu


def grafico_get_form(request):
    update_menu(request)

    context = {
        'title': 'Reportes consolidados (GRAFICOS)'
    }

    if request.method == 'GET':
        template = loader.get_template('reporte_graficos/solicitud_reporte.html')
    elif request.method == 'POST':
        template = loader.get_template('reporte_graficos/solicitud_reporte_detalle.html')

        fecha_inicio = request.POST.get('fecha_inicio', '12/01/2021')
        fecha_final = request.POST.get('fecha_final', '12/01/2021')

        fecha_inicio_ = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_final_ = datetime.datetime.strptime(fecha_final, '%Y-%m-%d')

        object_list = Solicitud.objects.filter(registrado_fecha__range=[fecha_inicio_, fecha_final_])

        covid_total = len(object_list.filter(es_covid=True))
        no_covid_total = len(object_list.filter(es_covid=False))

        covid_1 = len(object_list.filter(es_covid=True, estado=4))
        covid_2 = len(object_list.filter(es_covid=True, estado=1))

        no_covid_1 = len(object_list.filter(es_covid=False, estado=4))
        no_covid_2 = len(object_list.filter(es_covid=False, estado=1))

        autorizados = [covid_1, no_covid_1]
        pendientes = [covid_2, no_covid_2]

        totales = [covid_total, no_covid_total]

        count = Solicitud.objects.filter(registrado_fecha__range=[fecha_inicio_, fecha_final_]).count()

        solicitud_sn = ["1", "SOLICITUDES SIN NÚMERO DE EXPEDIENTE",
                        len(object_list.filter(es_covid=True, numero_expediente__exact='')),
                        len(object_list.filter(es_covid=False, numero_expediente__exact=''))]

        ss = object_list.filter(es_covid=True, numero_expediente__isnull=True)

        solicitud_cn = ["2", "SOLICITUDES CON NÚMERO DE EXPEDIENTE",
                        len(object_list.filter(es_covid=True, numero_expediente__exact='')),
                        len(object_list.filter(es_covid=False, numero_expediente__exact=''))]

        solicitud_at = ["5", "SOLICITUDES CERTIFICADAS", len(object_list.filter(es_covid=True, estado=5)),
                        len(object_list.filter(es_covid=False, estado=5))]

        # solicitud_pd = ["3", "SOLICITUDES PENDIENTES"] + [str(a_i - b_i) if (a_i - b_i) >= 0 else "0" for a_i, b_i in
        #                                                   zip(solicitud_cn[2:], solicitud_at[2:])]
        # solicitud_ob = ["4", "SOLICITUDES OBSERVADAS", len(object_list.filter(es_covid=True, estado=3)),
        #                 len(object_list.filter(es_covid=False, estado=3))]

        tabla_consolidado = [solicitud_sn, solicitud_cn, solicitud_at]

        tabla_consolidado_covid = [solicitud_sn[2], solicitud_cn[2], solicitud_at[2]]
        tabla_consolidado_no_covid = [solicitud_sn[3], solicitud_cn[3], solicitud_at[3]]

        context['object_list'] = object_list
        context['count'] = count
        context['fecha_inicio'] = fecha_inicio
        context['fecha_final'] = fecha_final
        context['autorizados'] = autorizados
        context['pendientes'] = pendientes
        context['totales'] = totales
        context['total'] = len(object_list)
        context['tabla_consolidado'] = tabla_consolidado
        context['tabla_consolidado_covid'] = tabla_consolidado_covid
        context['tabla_consolidado_no_covid'] = tabla_consolidado_no_covid

    return HttpResponse(template.render(context, request))
