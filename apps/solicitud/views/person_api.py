import os
import sys

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass

import json
from django.http import HttpResponse
from apps.util.get_person_api import get_person_api, get_person_api_reniec


def get_persona_by_dni(request, dni):
    """
    Vista para obtener la persona por DNI

    :param request:
    :param dni:
    :return: Persona en formato JSON
    """
    estado = True
    persona = ""
    if len(dni) == 8:
        persona = get_person_api(str(dni))
        if persona:
            if persona['dni'] == 'xxxxx':
                estado = False
        else:
            estado = False
    else:
        estado = False

    respuesta = {
        'estado': estado,
        'persona': persona,
    }
    return HttpResponse(json.dumps(respuesta), content_type='application/json')



def get_persona_by_dni_reniec(request, dni):
    """
    Vista para obtener la persona por DNI

    :param request:
    :param dni:
    :return: Persona en formato JSON
    """
    estado = True
    persona = ""
    if len(dni) == 8:
        persona = get_person_api_reniec(str(dni))
        if persona:
            if persona['dni'] == "xxxx":
                estado = False
        else:
            estado = False
    else:
        estado = False

    respuesta = {
        'estado': estado,
        'persona': persona,
    }
    return HttpResponse(json.dumps(respuesta), content_type='application/json')
