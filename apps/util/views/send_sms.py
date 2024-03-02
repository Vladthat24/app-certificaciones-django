import urllib.request
from urllib.parse import quote


def send_sms(cell_phone, text):
    try:
        text = quote(text.encode('utf-8'))
        url = "http://api.creasms.com/web/enviar.php?key=34567-26h12l18e16a50u13ifFaoa0VA&pais=51&movil=" + cell_phone + "&remitente=CreaSMS.com&mensaje=" + text + "&unicode=si"
        contents = str(urllib.request.urlopen(url).read())
        response = "El sms ha sido entregado al destinatario."
        if contents.find("-1") == 2:
            response = "SMS no entregado a destinatario, error general."
        if contents.find("-2") == 2:
            response = "sms no entregado, numero no existe."
        if contents.find("-3") == 2:
            response = "sms no entregado, expirado en operador."
        if contents.find("-5") == 2:
            response = "No tiene Activado envios Externos."
        if contents.find("-10") == 2:
            response = "IP No válida. "
        if contents.find("-15") == 2:
            response = "Error de autentificación. "
        if contents.find("-20") == 2:
            response = "No dispone de Créditos suficientes para realizar el envío. "
        if contents.find("-25") == 2:
            response = "No es posible enviar el sms a ese Pais. "
        if contents.find("-30") == 2:
            response = "El número al que desea enviar, es incorrecto. "
        if contents.find("-35") == 2:
            response = "El Remitente que desea usar, no esta activo o validado."
        if contents.find("-40") == 2:
            response = "El texto a enviar es superior al permitido (160) "
        if contents.find("-50") == 2:
            response = "El Pais al que intentas enviar no está autorizado. "
        if contents.find("-100") == 2:
            response = "Error Genérico, faltan parametros o error desconocido. "
        return response
    except AttributeError:
        return "Error de sintaxis"
