import asyncio
import time
from json import JSONDecodeError

import requests
from rest_framework.utils import json


async def send_email(correo_para, cliente_nombre, mensaje):
    headers = {
        'Authorization': 'token 3dae27e1b9702aefa8341474b9e422cc8ca2cad6'
    }
    data = {
        'para': correo_para,
        'copia': "mendoza.oscar.david@gmail.com",
        'cliente_nombre': cliente_nombre,
        'mensaje': mensaje
    }
    r = requests.post('https://api.matricula.edu.pe/api/send-email', headers=headers, data=data)
    try:
        response_dict = json.loads(r.text)
    except JSONDecodeError:
        return {"Error al enviar"}


async def send_sms(para, mensaje):
    headers = {
        'Authorization': 'token 3dae27e1b9702aefa8341474b9e422cc8ca2cad6'
    }
    data = {
        'para': para,
        'mensaje': mensaje
    }
    r = requests.post('https://api.matricula.edu.pe/api/send-sms', headers=headers, data=data)
    try:
        response_dict = json.loads(r.text)
    except JSONDecodeError:
        return {"Error al enviar SMS"}


async def send_main_asynchronous(correo, celular, cliente_nombre, mensaje):
    task_1 = asyncio.create_task(
        send_email(correo, cliente_nombre, mensaje))

    task_2 = asyncio.create_task(
        send_sms(celular, mensaje))
    # task_2 = asyncio.create_task(send_sms())

    print(f"start {time.strftime('%X')}")
    await task_1
    await task_2
    # await task_2
    print(f"end {time.strftime('%X')}")
