import os

import pandas as pd

from apps.solicitud.models.hospital import Hospital


def run_file_hospital():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_excel(BASE_DIR + '/load_excel/listado.xlsx', engine='openpyxl',
                       dtype={'Código Único': 'string', 'Nombre del establecimiento': 'string', 'Dirección': 'string'})

    list_zip = zip(df["Código Único"], df["Nombre del establecimiento"], df["Dirección"])

    for codigo_unico, nombre, direccion in list_zip:
        try:
            hospital = Hospital.objects.get(codigo_unico=codigo_unico.strip())
            hospital.direccion = direccion.strip()
            hospital.save()

        except Hospital.DoesNotExist:
            print(" No encontrado ******* ****")
