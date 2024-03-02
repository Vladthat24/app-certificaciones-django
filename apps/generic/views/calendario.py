import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.generic.models.calendario_feriado import CalendarioFeriado
from apps.util.update_menu import update_menu


def calendario_serializer(calendario):
    return {'id': calendario.id, 'title': calendario.title, 'date': calendario.date.strftime("%Y-%m-%d"),
            'type': calendario.type}


def calendar_view(request):
    """
    Vista para obtener obtener el calendario

    :param request:
    :param dni:
    :return: Persona en formato JSON
    """

    update_menu(request)

    return render(request, 'generic/calendario.html', {'title': " Calendario"})


def lista_calendario(request):
    return HttpResponse(json.dumps(get_all()), content_type='application/json')


@csrf_exempt
def actualizar_calendario(request):
    json_data = json.loads(request.body)

    try:
        CalendarioFeriado.objects.get(date=datetime.strptime(json_data["date"], '%Y-%m-%d')).delete()
    except CalendarioFeriado.DoesNotExist:
        CalendarioFeriado.objects.update_or_create(date=datetime.strptime(json_data["date"], '%Y-%m-%d'))

    return HttpResponse(json.dumps(get_all()), content_type='application/json')


def get_all():
    lista_calendario = CalendarioFeriado.objects.all()

    lista_calendario_json = [calendario_serializer(i) for i in lista_calendario]

    return lista_calendario_json
