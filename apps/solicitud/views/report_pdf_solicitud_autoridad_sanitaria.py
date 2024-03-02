import os
import sys

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass
    # django.setup()

from datetime import datetime
from io import BytesIO

from django.conf import settings
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, TableStyle
from reportlab.platypus import Table
from reportlab.platypus.flowables import Spacer

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import locale

locale.setlocale(locale.LC_TIME, "es_ES")

styles = getSampleStyleSheet()

sp_title_1 = ParagraphStyle('parrafos',
                            alignment=TA_CENTER,
                            fontSize=11,
                            fontName="Calibri-Bold")

sp_subtitle = ParagraphStyle('parrafos',
                             alignment=TA_CENTER,
                             fontSize=8,
                             leading=15,
                             fontName="Calibri-Bold")

sp_justifi_title_table = ParagraphStyle('parrafos',
                                        alignment=TA_JUSTIFY,
                                        fontSize=10,
                                        leading=10,
                                        fontName="Calibri-Bold")

sp_parrafo = ParagraphStyle('parrafos',
                            alignment=TA_JUSTIFY,
                            fontSize=10,
                            leading=12,
                            fontName="Calibri-Regular")

sp_parrafo_right = ParagraphStyle('parrafos',
                                  alignment=TA_RIGHT,
                                  fontSize=10,
                                  leading=12,
                                  fontName="Calibri-Regular")

sp_justifi_title_table_center = ParagraphStyle('parrafos',
                                               alignment=TA_CENTER,
                                               fontSize=10,
                                               fontName="Times-Roman")

sp_justifi_title_header = ParagraphStyle('parrafos',
                                         alignment=TA_CENTER,
                                         fontSize=7,
                                         # leading=10,
                                         fontName="Times-Roman")

sp_justifi_title_body = ParagraphStyle('parrafos',
                                       alignment=TA_RIGHT,
                                       fontSize=7,
                                       # leading=10,
                                       fontName="Times-Roman")


class ReportSolicitudAutoridadSanitaria():
    # tea = Tea.objects.get(pk=1)

    def __init__(self, pagesize, solicitud):

        self.buffer = BytesIO()
        self.solicitud = solicitud
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.height, self.width = self.pagesize

    def listToString(self, s):
        str1 = ""
        for ele in s:
            str1 += ele[2:]
        return str1

    def tabla_encabezado(self, styles):
        now = datetime.now()
        sp = ParagraphStyle('parrafos',
                            alignment=TA_CENTER,
                            fontSize=16,
                            fontName="Times-Roman",
                            leading=20
                            )
        sp_date = ParagraphStyle('parrafos',
                                 alignment=TA_RIGHT,
                                 fontSize=15,
                                 fontName="Times-Roman",
                                 )
        # sp = ParagraphStyle('parrafos',
        #                     alignment=TA_CENTER,
        #                     fontSize=16,
        #                     fontName="Times-Roman",
        #                     )
        try:
            archivo_imagen = os.path.join(settings.STATIC_LOCAL_ROOT, "img/logo_solicitud_1.png")
            imagen = Image(archivo_imagen, width=230, height=35)
        except:
            imagen = Paragraph(u"LOGO", sp)

        encabezado = [[imagen]]
        tabla_encabezado = Table(encabezado, colWidths=[18 * cm])

        tabla_encabezado.setStyle(TableStyle(
            [
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                # ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                # ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
                # ('ALIGN', (0, 0), (2, 0), 'CENTER'),
                # ('VALIGN', (0, 0), (2, 0), 'CENTER'),
                # ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                # ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
            ]
        ))
        return tabla_encabezado

    def tabla_titulo_main(self, styles):

        titulo = Paragraph(u"SOLICITUD DE AUTORIZACION SANITARIA PARA CREMACIÓN DE CADAVER <br/>"
                           u"<font name='Calibri-Bold' size='8'>(Solicitud con carácter de Declaración Jurada)</font>",
                           sp_title_1)
        titulo_director = Paragraph(
            u"SEÑOR (A):<br/> DIRECTOR(A) GENERAL DE LA DIRECCIÓN DE REDES INTEGRADAS DE SALUD LIMA SUR.<br/> S.D.",
            sp_justifi_title_table)

        encabezado = [[titulo], [titulo_director]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_parrafo_uno(self, styles):

        titulo_director = Paragraph(
            u"Yo: <font name='Calibri-Regular' size='10'> AUTORIDAD SANITARIA </font>"
            + " a usted atentamente digo: ",
            sp_parrafo)

        tabla = Table([[titulo_director]])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_parrafo_dos(self, styles):

        titulo_director = Paragraph(
            u"Que, al amparo de lo establecido en la Ley Nº 26298, Ley de Cementerios y Servicios"
            u" Funerarios y su Reglamento aprobado mediante D.S. Nº 03-94-SA, solicito a su despacho realizar "
            u"el trámite para obtener la Autorización Sanitaria de CREMACIÓN DE CADÁVER, de quién en vida fue:  ",
            sp_parrafo)

        tabla = Table([[titulo_director]])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_parrafo_tres(self, styles):

        crematorio_nombre = self.solicitud.crematorio.nombre.upper() if self.solicitud.crematorio else " - "
        crematorio_direccion = self.solicitud.crematorio.direccion.upper() if self.solicitud.crematorio else " - "
        crematorio_distrito = self.solicitud.crematorio.distrito.name.upper() if self.solicitud.crematorio else " - "
        crematorio_provincia = self.solicitud.crematorio.distrito.province.name.upper() if self.solicitud.crematorio else " - "
        crematorio_departamento = self.solicitud.crematorio.distrito.province.department.name.upper() if self.solicitud.crematorio else " - "

        preposicion_titulo = " en el(la) <font name='Calibri-Regular' size='10'>" + self.solicitud.get_lugar_fallecimiento_tipo_display() + "</font>, "
        if self.solicitud.lugar_fallecimiento_preposicion_titulo:
            preposicion_titulo = self.solicitud.lugar_fallecimiento_preposicion_titulo + ", "
        nombre_hospital = ""

        if self.solicitud.lugar_fallecimiento_tipo == 1:
            nombre_hospital = " " + self.solicitud.get_hospital_nombre() + ", "

        distrito_name = " Provincia de " + self.solicitud.get_direccion_fallecimiento()[
            "provincia"].upper() + "," + "  y Departamento de " + \
                        self.solicitud.get_direccion_fallecimiento()["departamento"].upper() + ", "

        if self.solicitud.get_direccion_fallecimiento()["provincia_id"] == 701:
            distrito_name = " en la " + self.solicitud.get_direccion_fallecimiento()[
                "provincia"].upper() + ", "



        fallecido_numero_documento = " - "

        if self.solicitud.fallecido_numero_documento:
            fallecido_numero_documento = self.solicitud.fallecido_numero_documento

        titulo_director = Paragraph(
            u"Don(ña): <font name='Calibri-Regular' size='10'>" + self.solicitud.get_fallecido().upper() + "</font>"
            + " identificado (a) con  <font name='Calibri-Regular' size='10'>" + self.solicitud.get_fallecido_tipo_documento_display() + "</font> "
            + fallecido_numero_documento
            + " quien falleció el día <font name='Calibri-Regular' size='10'>" + self.solicitud.fallecido_fecha_fallecimiento.strftime(
                "%d %B, %Y") + "</font> ,"
            + " a horas <font name='Calibri-Regular' size='10'>" + self.solicitud.fallecido_hora_fallecimiento + "</font>, "
            + preposicion_titulo
            + nombre_hospital
            + " ubicado en " + self.solicitud.get_direccion_fallecimiento()["direccion"].upper() + ", "
            + " distrito de " + self.solicitud.get_direccion_fallecimiento()["distrito"].upper() + ", "
            + distrito_name
            + " para ser cremado en el crematorio: " + crematorio_nombre + ", "
            + " ubicado en " + crematorio_direccion + ", "
            + " distrito de " + crematorio_distrito + ","
            + " provincia de " + crematorio_provincia + ","
            + " departamento de " + crematorio_departamento + ".",
            sp_parrafo)

        tabla = Table([[titulo_director]])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_parrafo_cuatro(self, styles):

        titulo_director = Paragraph(
            u"En ese sentido, <font name='Calibri-Bold' size='10'>DECLARO BAJO JURAMENTO</font>"
            + ", conforme a la prelación establecida en el artículo 236° del código civil;"
            + " de igual forma, declaro bajo juramento, ser responsable de la veracidad de los documentos e "
            + "información que presento en el procedimiento, de conformidad a lo establecido con el principio de presunción "
            + "de veracidad establecido en el numeral 1.7 del artículo IV del Título Preliminar del T.U.O. de la Ley Nº 27444, "
            + "Ley del Procedimiento Administrativo General, aprobado mediante Decreto Supremo N° 004-2019-JUS, sujetándome a "
            + "las responsabilidades civiles, penales y administrativas que correspondan, en caso de comprobarse su falsedad, "
            + "del mismo modo, declaro cumplir con todos los requisitos establecidos en el TUPA/MINSA. ",
            sp_parrafo)

        tabla = Table([[titulo_director]])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_parrafo_requisitos(self, styles):

        titulo_director = Paragraph(
            u"Asimismo, para el trámite se adjunta los siguientes requisitos:  <br/>"
            + "<font name='Calibri-Bold' size='10'>1. Muerte Natural (   ) </font> <br/>"
            + "<font name='Calibri-Bold' size='10'>1.1</font> Copia simple del DNI, Carnet de Extranjería o Pasaporte del solicitante, según corresponda. (   ) <br/>"
            + "<font name='Calibri-Bold' size='10'>1.2</font> Copia simple del Certificado de defunción (  )<br/>"
            + "<font name='Calibri-Bold' size='10'>1.3</font> Certificado y Protocolo de Necropsia, suscrito por el Médico Anátomo-Patólogo, según corresponda (  ) <br/>"
            + "<font name='Calibri-Bold' size='10'>2.Muerte Súbita o Violenta (   ) </font> <br/>"
            + "<font name='Calibri-Bold' size='10'>2.1</font> Copia simple del DNI, Carnet de Extranjería o Pasaporte del solicitante, según corresponda. (  )<br/>"
            + "<font name='Calibri-Bold' size='10'>2.2</font> Copia simple del Certificado y Protocolo de Necropsia, suscrito por el Médico Legista. (  )<br/>"
            + "<font name='Calibri-Bold' size='10'>2.3</font> Copia simple del Certificado de la Autorización del Fiscal Provincial, en caso de ingresar a la morgue (accidente, suicidio o crimen) (  ).<br/>"
            + "<font name='Calibri-Regular' size='8'>* En ambos casos, se deberá Indicar la fecha y N° de operación de la constancia de pago o copia del mismo; en caso de pagos masivos, se deberá"
            + "adjuntar una declaración jurada de pago y la relación de los fallecidos por los cuales se solicita la autorización sanitaria. </font>",
            sp_parrafo)

        tabla = Table([[titulo_director]])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_parrafo_expuesto(self, styles):

        texto = Paragraph(
            u"<font name='Calibri-Bold' size='10'> POR LO EXPUESTO:</font> <br/>"
            + "Se brinde la atención al presente, en el plazo de Ley.",
            sp_parrafo)

        texto_uno = Paragraph(
            u"Barranco, " + datetime.now().strftime("%d %B, %Y"),
            sp_parrafo_right)

        tabla = Table([[texto], [texto_uno]])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_firma(self, styles):

        try:
            archivo_imagen = os.path.join(settings.STATIC_LOCAL_ROOT, "img/huella.png")
            imagen = Image(archivo_imagen, width=50, height=60)
        except:
            imagen = Paragraph(u"LOGO", sp_justifi_title_table)

        data = [
            [Paragraph(u"…………………………………", sp_justifi_title_table), imagen],
            [Paragraph(u"Firma Del Solicitante", sp_justifi_title_table), " X"],
            [" ", " X"],
            [" ", " X"]
        ]

        tabla = Table(data, colWidths=[4 * cm, 2 * cm], rowHeights=(0.4 * cm, 0.4 * cm, 0.4 * cm, 0.4 * cm))
        tabla.setStyle(TableStyle(
            [
                ('SPAN', (1, 0), (1, 3)),
                # ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.black),
                # ('BOX', (0, 0), (-1, -1), 0.1, colors.black),
                # ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                # ('VALIGN', (0, 0), (0, -1), 'TOP'),

            ]
        ))
        return tabla

    def imprimir(self):

        pdfmetrics.registerFont(
            TTFont('Roboto-Regular', os.path.join(settings.STATIC_LOCAL_ROOT, "fonts/Roboto-Regular.ttf")))
        pdfmetrics.registerFont(
            TTFont('Roboto-Bold', os.path.join(settings.STATIC_LOCAL_ROOT, "fonts/Roboto-Bold.ttf")))
        pdfmetrics.registerFont(
            TTFont('Roboto-Italic', os.path.join(settings.STATIC_LOCAL_ROOT, "fonts/Roboto-Italic.ttf")))
        pdfmetrics.registerFont(
            TTFont('Roboto-BoldItalic', os.path.join(settings.STATIC_LOCAL_ROOT, "fonts/Roboto-BoldItalic.ttf")))

        pdfmetrics.registerFont(
            TTFont('Calibri-Regular', os.path.join(settings.STATIC_LOCAL_ROOT, "fonts/Calibri-Regular.ttf")))
        pdfmetrics.registerFont(
            TTFont('Calibri-Bold', os.path.join(settings.STATIC_LOCAL_ROOT, "fonts/Calibri-Bold.ttf")))
        pdfmetrics.registerFont(
            TTFont('Calibri-Italic', os.path.join(settings.STATIC_LOCAL_ROOT, "fonts/Calibri-Italic.ttf")))
        pdfmetrics.registerFont(
            TTFont('Calibri-BoldItalic', os.path.join(settings.STATIC_LOCAL_ROOT, "fonts/Calibri-Bold-Italic.ttf")))

        pdfmetrics.registerFontFamily(
            'Roboto',
            normal='Roboto-Regular',
            bold='Roboto-Bold',
            italic='Roboto-Italic',
            boldItalic='Roboto-BoldItalic')

        pdfmetrics.registerFontFamily(
            'Calibri',
            normal='Calibri-Regular',
            bold='Calibri-Bold',
            italic='Calibri-Italic',
            boldItalic='Calibri-BoldItalic')

        buffer = self.buffer
        lWidth, lHeight = A4

        doc = SimpleDocTemplate(buffer,
                                rightMargin=60,
                                leftMargin=60,
                                topMargin=15,
                                bottomMargin=15,
                                pagesize=(lWidth, lHeight))

        doc.title = " SOLICITUD DE AUTORIZACION SANITARIA PARA CREMACIÓN DE CADAVER"

        elements = []
        styles = getSampleStyleSheet()
        elements.append(self.tabla_encabezado(styles))
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(self.tabla_titulo_main(styles))
        elements.append(Spacer(1, 0.4 * cm))
        elements.append(self.tabla_parrafo_uno(styles))
        elements.append(Spacer(1, 0.1 * cm))
        elements.append(self.tabla_parrafo_dos(styles))
        elements.append(Spacer(1, 0.1 * cm))
        elements.append(self.tabla_parrafo_tres(styles))
        elements.append(Spacer(1, 0.1 * cm))
        elements.append(self.tabla_parrafo_cuatro(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_parrafo_requisitos(styles))
        elements.append(Spacer(1, 0.25 * cm))
        elements.append(self.tabla_parrafo_expuesto(styles))
        elements.append(Spacer(1, 2 * cm))
        elements.append(self.tabla_firma(styles))
        elements.append(Spacer(1, 0.25 * cm))

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
