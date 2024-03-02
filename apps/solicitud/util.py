from datetime import datetime, timedelta, time

from apps.generic.models.calendario_feriado import CalendarioFeriado
from apps.generic.models.rango_horario import RangoHorario



def dateSetValues(today, numberDate):
    today -= timedelta(minutes=today.hour * 60 + (today.minute - 2))
    today += timedelta(days=numberDate)
    return today


def get_fecha_registrado_valid(today):

    hora_limite = time(23, 15, 00)

    if today.time() > hora_limite:
       today = dateSetValues(today,1)

    if today.weekday() == 5:
        today = dateSetValues(today, 2)
        # return today
    if today.weekday() == 6:
        today = dateSetValues(today,1)
        # return today
    # if today.weekday() < 5:
    #     return today

    return today


def get_fecha_excluyendo_no_laborables():
    now = datetime.now()

    date_inicio = datetime.strptime('07/27/22 16:15:00', '%m/%d/%y %H:%M:%S')
    date_fin = datetime.strptime('07/30/22 08:00:00', '%m/%d/%y %H:%M:%S')

    if now > date_inicio and now < date_fin:
        return datetime.strptime('08/01/22 00:00:01', '%m/%d/%y %H:%M:%S')

    now_new = datetime.now()

    if now.weekday() in [5, 6]:
        if now.weekday() == 5:
            if now.hour > 11:
                now_new = now_new + timedelta(days=2)
            else:
                return now
        else:
            now_new = now_new + timedelta(days=1)

        return now_new.replace(hour=8, minute=0, second=0)
    else:
        return now


def es_feriado(date):
    lista_feriados = CalendarioFeriado.objects.filter(date=date)

    if len(lista_feriados) > 0:
        return get_fecha_excluyendo_no_laborables_two(date + timedelta(days=1))
    elif date.date() == datetime.now().date():
        return date
    else:
        return date - timedelta(minutes=date.hour * 60 + (date.minute - 2))


def get_fecha_excluyendo_no_laborables_two(today):
    try:
        rango_horario = RangoHorario.objects.get(state=True)
        hora_limite = rango_horario.rango
    except RangoHorario.DoesNotExist:
        hora_limite = time(16, 15, 00)


    if today.date() == datetime.now().date() and today.time() > hora_limite:
        today -= timedelta(minutes=today.hour * 60 + (today.minute - 2))
        today += timedelta(days=1)

    if today.weekday() == 5:
        today += timedelta(days=2)
        return es_feriado(today)
    if today.weekday() == 6:
        today += timedelta(days=1)
        return es_feriado(today)
    if today.weekday() < 5:
        return es_feriado(today)
