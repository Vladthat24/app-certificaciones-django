
from apps.util.get_person_api import *

def get_sexo_solicitante(certificado):
        
    persona = get_person_api_reniec(certificado.solicitud.solicitante_numero_documento);
    solicitante_sexo = 1

    if persona and persona != 'Ingrese un DNI con 8 digitos':
        try:
            if persona['dni'] == "xxxx":
                if certificado.solicitud.solicitante_nombres[-1] == 'A' or certificado.solicitud.solicitante_nombres[-1] == 'a':
                    solicitante_sexo = 2
                else:
                    pass
            else:
                solicitante_sexo = int(persona['sexo'])
        except Exception as e:
            print("error")
    else:
        if certificado.solicitud.solicitante_nombres[-1] == 'A' or certificado.solicitud.solicitante_nombres[-1] == 'a':
            solicitante_sexo = 2
        else:
            pass

    return solicitante_sexo