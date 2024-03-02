import locale
import os
from datetime import datetime
from io import BytesIO

from django.conf import settings
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_JUSTIFY
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, TableStyle, PageBreak
from reportlab.platypus import Table
from reportlab.platypus.flowables import Spacer

from apps.generic.models.resolucion import Resolucion

locale.setlocale(locale.LC_TIME, "es_ES")

styles = getSampleStyleSheet()

sp_title_1 = ParagraphStyle('parrafos',
                            alignment=TA_CENTER,
                            fontSize=14,
                            fontName="Calibri-Bold")

sp_subtitle = ParagraphStyle('parrafos',
                             alignment=TA_CENTER,
                             fontSize=8,
                             leading=15,
                             fontName="Calibri-Bold")

sp_justifi_title_table = ParagraphStyle('parrafos',
                                        alignment=TA_JUSTIFY,
                                        fontSize=11,
                                        leading=12,
                                        fontName="Calibri-Regular")

sp_parrafo = ParagraphStyle('parrafos',
                            alignment=TA_JUSTIFY,
                            fontSize=11,
                            leading=10,
                            fontName="Calibri-Regular")

sp_parrafo_right = ParagraphStyle('parrafos',
                                  alignment=TA_RIGHT,
                                  fontSize=10,
                                  leading=12,
                                  fontName="Calibri-Regular")

sp_parrafo_right_bold = ParagraphStyle('parrafos',
                                       alignment=TA_RIGHT,
                                       fontSize=12,
                                       leading=12,
                                       fontName="Calibri-Bold")

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


class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.setFont(self, 'Times-Roman', 2, None)
            canvas.Canvas.showPage(self)

            # def setFont(self, psfontname, size, leading=None):

        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.setFont("Helvetica", 8)
        self.drawCentredString(30 * mm, 1 * mm + (0.2 * inch), "Página %d de %d" % (self._pageNumber, page_count))

        # self.drawCentredString(30 * mm, 1 * mm + (0.2 * inch), imagen)


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 8)
    page_number_text = "Página %d" % (doc.page)
    canvas.drawCentredString(
        0.80 * inch,
        0.80 * inch,
        page_number_text
    )
    canvas.restoreState()


class ReportCertificadoAutoridadSanitaria():
    # tea = Tea.objects.get(pk=1)

    def __init__(self, pagesize, certificado, solicitante_sexo):

        self.buffer = BytesIO()
        self.certificado = certificado
        self.solicitante_sexo = solicitante_sexo
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.height, self.width = self.pagesize


        self.tenor_solicitante = "don"
        self.valor_identificado_solicitante = 'identificado'
        self.tenor_fallecido = "don"
        self.valor_fallecido = 'fallecido'

        if solicitante_sexo == 2:
            self.tenor_solicitante = "doña"
            self.valor_identificado_solicitante = 'identificada'

        if certificado.solicitud.fallecido_sexo == 2:
            self.tenor_fallecido = "doña"
            self.valor_fallecido = 'fallecida'

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
            archivo_imagen = os.path.join(settings.STATIC_LOCAL_ROOT, "img/logo_certificaciones.jpg")
            imagen = Image(archivo_imagen, width=470, height=45)
        except:
            imagen = Paragraph(u"LOGO", sp)

        encabezado = [[imagen]]
        tabla_encabezado = Table(encabezado, colWidths=[17 * cm])

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

    def tabla_numero_expediente(self, styles):

        nro_expediente = "--"
        if self.certificado.solicitud.numero_expediente:
            nro_expediente = self.certificado.solicitud.numero_expediente

        texto_uno = Paragraph(
            u"N° " + self.certificado.numero_autorizacion + " <br/> <br/>  "
                                                            " Expediente Nº " + str(nro_expediente),
            sp_parrafo_right_bold)

        tabla = Table([[texto_uno]])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_titulo_main(self, styles):

        nro_expediente = "--"
        if self.certificado.solicitud.numero_expediente:
            nro_expediente = self.certificado.solicitud.numero_expediente

        titulo = Paragraph(u"AUTORIZACIÓN SANITARIA PARA CREMACIÓN DE CADÁVER<br/><br/>",
                           sp_title_1)
        titulo_visto = Paragraph(
            u"<font name='Calibri-Bold' size='12'>VISTO: </font>",
            sp_justifi_title_table)

        titulo_presenta = Paragraph(
            u"El expediente N° <font name='Calibri-Bold' size='12'>" + nro_expediente + "</font> , "
            + " recepcionado el " + self.certificado.solicitud.registrado_fecha.strftime("%d de %B del %Y") + ", "
            + " por la oficina de Trámite Documentario de la DIRIS Lima Sur, presentado por la "
            + " <font name='Calibri-Bold' size='12'> AUTORIDAD SANITARIA </font>, y; ",
            sp_justifi_title_table)

        encabezado = [[titulo], [titulo_visto], [titulo_presenta]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_antecedentes_main(self, styles):

        nombre_hospital = ""
        if self.certificado.solicitud.lugar_fallecimiento_tipo == 1:
            nombre_hospital = " " + self.certificado.solicitud.get_hospital_nombre() + ", "

        distrito_name = " Provincia de " + self.certificado.solicitud.get_direccion_fallecimiento()[
            "provincia"] + "," + "  y Departamento de " + \
                        self.certificado.solicitud.get_direccion_fallecimiento()["departamento"] + ", "

        if self.certificado.solicitud.get_direccion_fallecimiento()["provincia_id"] == 701:
            distrito_name = " en la " + self.certificado.solicitud.get_direccion_fallecimiento()[
                "provincia"] + ", "

        preposicion_titulo = " en el(la) " + self.certificado.solicitud.get_lugar_fallecimiento_tipo_display() + ", "
        if self.certificado.solicitud.lugar_fallecimiento_preposicion_titulo:
            preposicion_titulo = self.certificado.solicitud.lugar_fallecimiento_preposicion_titulo + ", "

        titulo_antecedentes = Paragraph(
            u"<font name='Calibri-Bold' size='12'>CONSIDERANDO: </font>",
            sp_justifi_title_table)
        titulo_presenta = Paragraph(
            u"Que, mediante el documento de la referencia, <font name='Calibri-Bold' size='11'>"
            u"LA AUTORIDAD SANITARIA </font>, solicita la autorización sanitaria"
            + " para la cremación del cadáver de: "
            + "<font name='Calibri-Bold' size='11'>" + self.certificado.solicitud.get_fallecido() + "</font>, "
            + self.valor_fallecido + " el día " + self.certificado.solicitud.fallecido_fecha_fallecimiento.strftime(
                "%d de %B del %Y") + ", "
            + preposicion_titulo
            + nombre_hospital
            + " sito en " + self.certificado.fallecido_direccion + ", "
            + " del distrito de " + self.certificado.solicitud.get_direccion_fallecimiento()["distrito"] + ", "
            + distrito_name
            + "siendo la causa de muerte: <font name='Calibri-Bold' size='11'>"
            + self.certificado.motivo + "</font>, "
            + "según consta en el Certificado de Defunción obrante en el expediente. ",
            sp_justifi_title_table)

        encabezado = [[titulo_antecedentes], [titulo_presenta]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_body_estatico(self, styles):

        parrafo_uno = Paragraph(
            u"Que, mediante Decreto Supremo N° 008-2020-SA, se declara en emergencia sanitaria a nivel nacional, por el plazo de noventa (90) días calendario, por la existencia del COVID-19, la cual es prorrogada mediante Decretos Supremos Nº 020-2020-SA, N° 027-2020-SA, N° 031-2020-SA y prorrogada a partir del 7 de marzo de 2021, por un plazo de ciento ochenta (180) días calendario, mediante el Decreto Supremo N° 009-2021-SA. ",
            sp_justifi_title_table)

        parrafo_dos = Paragraph(
            u"En ese sentido, mediante Resolución Ministerial N° 100-2020-MINSA, se aprobó la Directiva Sanitaria N° 087-MINSA/2020/DIGESA, denominada "
            + "<font name='Calibri-Italic' size='11'>“Directiva Sanitaria para el Manejo de Cadáveres por COVID - 19”</font>,"
            + " modificada mediante las Resolución Ministeriales N° 171-2020/MINSA, N° 189-2020/MINSA y N° 208-2020/MINSA, la misma que señala: “Para la Inhumación o <u> cremación </u>de cadáveres con covid-19 o caso sospechoso, se deberá contar con el certificado de defunción y copia del DNI o carnet de extranjería, <u>los demás documentos que se requieren serán subsanados al término de la emergencia sanitaria</u>.”"
            + " así mismo, establece que ante la ausencia de familiares directos del fallecido por COVID 19 o bajo sospecha es la autoridad sanitaria la que autoriza la cremación.",
            sp_justifi_title_table)

        parrafo_tres = Paragraph(
            u"Que, los documentos obrantes en el expediente administrativo han sido presentados en copia simple por lo que de conformidad al principio de presunción de veracidad establecido en el numeral 1.7. del artículo IV del Título Preliminar del T.U.O. de la Ley N° 27444, Ley del Procedimiento Administrativo General, aprobado mediante Decreto Supremo N° 004-2019-JUS, los documentos y declaraciones formulados por los administrados responden a la verdad de los hechos que ellos afirman, reservándose la autoridad administrativa, el derecho de comprobar la veracidad de la información presentada de conformidad con el principio de privilegio de controles posteriores establecido en el numeral 1.16 del mismo artículo y norma administrativa descrita anteriormente..",
            sp_justifi_title_table)

        parrafo_cuatro = Paragraph(
            u"Asimismo, el numeral 17.1. del artículo 17 del T.U.O de la Ley N° 27444, Ley del Procedimiento Administrativo General, establece que, la autoridad podrá disponer en el mismo acto administrativo que tenga eficacia anticipada a su emisión, sólo si fuera más favorable a los administrados, y siempre que no lesione derechos fundamentales o intereses de buena fe legalmente protegidos a terceros.",
            sp_justifi_title_table)

        resolucion = Resolucion.objects.filter(estado=True)
        resolucion_nombre = 'N° 287-2021-DIRIS-LS/DG'
        if len(resolucion) > 0:
            resolucion_nombre = resolucion[0].resolucion

        parrafo_cinco = Paragraph(
            u"Por lo expuesto, de conformidad con lo establecido en las normas y directivas de gestión de la materia y de conformidad a la Resolución Directoral " + resolucion_nombre + ", que designa al suscrito como Director Ejecutivo de la Dirección de Salud Ambiental e Inocuidad Alimentaria de la Dirección de Redes Integradas de Salud Lima Sur, SE AUTORIZA A:",
            sp_justifi_title_table)

        encabezado = [[parrafo_uno], [parrafo_dos], [parrafo_tres], [parrafo_cuatro], [parrafo_cinco]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_fallecido(self, styles):
        nombre_hospital = ""
        if self.certificado.solicitud.lugar_fallecimiento_tipo == 1:
            nombre_hospital = " " + self.certificado.solicitud.get_hospital_nombre() + ", "

        distrito_name = " Provincia de " + self.certificado.solicitud.get_direccion_fallecimiento()[
            "provincia"] + "," + "  y Departamento de " + \
                        self.certificado.solicitud.get_direccion_fallecimiento()["departamento"] + ", "

        if self.certificado.solicitud.get_direccion_fallecimiento()["provincia_id"] == 701:
            distrito_name = " en la " + self.certificado.solicitud.get_direccion_fallecimiento()[
                "provincia"] + ", "

        preposicion_titulo = " en el(la) " + self.certificado.solicitud.get_lugar_fallecimiento_tipo_display() + ", "
        if self.certificado.solicitud.lugar_fallecimiento_preposicion_titulo:
            preposicion_titulo = self.certificado.solicitud.lugar_fallecimiento_preposicion_titulo + ", "

        titulo_presenta = Paragraph(
            u"La <font name='Calibri-Bold' size='11'> AUTORIDAD SANITARIA </font>, "
            + "para Cremar el Cadáver de:"
            + " <font name='Calibri-Bold' size='11'>" + self.certificado.solicitud.get_fallecido() + "</font>, "
            + self.valor_fallecido + " el día " + self.certificado.solicitud.fallecido_fecha_fallecimiento.strftime(
                "%d de %B del %Y") + ", "
            + preposicion_titulo
            + nombre_hospital
            + " sito en " + self.certificado.fallecido_direccion + ", "
            + " del distrito de " + self.certificado.solicitud.get_direccion_fallecimiento()["distrito"] + ", "
            + distrito_name
            + " cuya causa de muerte fue: <font name='Calibri-Bold' size='11'>"
            + self.certificado.motivo + "</font>, "
            + " según consta en el Certificado de Defunción adjunto al presente, para ser incinerado en el Crematorio: "
            + self.certificado.solicitud.crematorio.nombre + ".", sp_justifi_title_table)

        encabezado = [[titulo_presenta]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_dispone(self, styles):

        titulo_presenta = Paragraph(
            u"<font name='Calibri-Bold' size='12'>SE DISPONE: </font> Que, la Gerencia y/o Administración responsable del Crematorio, cumpla con lo establecido en la Directiva Sanitaria N° 087-MINSA/2020/DIGESA, “Directiva Sanitaria para el Manejo de Cadáveres por COVID - 19”; asimismo, remita un Acta de Acreditación del procedimiento realizado debidamente firmada en un plazo máximo de diez (10) días útiles.",
            sp_justifi_title_table)

        encabezado = [[titulo_presenta]]
        tabla = Table(encabezado)
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_exhorta(self, styles):
        titulo_presenta = Paragraph(
            u"<font name='Calibri-Bold' size='12'>SE DISPONE: </font> Que, la Gerencia y/o Administración responsable "
            + " del Crematorio, cumpla con lo establecido en la Directiva Sanitaria Nª 087-MINSA/2020/DIGESA,"
            + "<font name='Calibri-Italic' size='11'> “Directiva Sanitaria para el Manejo de Cadáveres por COVID - 19”</font>;"
            + " asimismo, remita un Acta de Acreditación del preocedimiento realizado debidamente firmada en un plazo máximo de diez (10)"
            + " días útiles.",
            sp_justifi_title_table)

        encabezado = [[titulo_presenta]]
        tabla = Table(encabezado)
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_parrafo_fecha(self, styles):

        texto_uno = Paragraph(
            u"Barranco, " + self.certificado.solicitud.registrado_fecha.strftime("%d de %B del %Y") + ".",
            sp_parrafo_right)

        tabla = Table([[texto_uno]])
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    def tabla_parrafo_pie_pagina(self, styles):

        texto_uno = Paragraph(
            u"<font name='Calibri-Regular' size='9'>EJSH/MMHV/</font><br/>"
            + "<font name='Calibri-Bold' size='9'> <u>  DISTRIBUCIÓN:</u> </font><br/> "
            + "<font name='Calibri-Regular' size='9'> ( 1 ) Interesado</font><br/> "
            + "<font name='Calibri-Regular' size='9'> ( 1 ) DSAIA (1° copia)</font> ",
            sp_parrafo)

        tabla = Table([[texto_uno]])
        tabla.setStyle(TableStyle(
            []
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
                                topMargin=25,
                                bottomMargin=60,
                                pagesize=(lWidth, lHeight))

        doc.title = " AUTORIZACIÓN SANITARIA PARA CREMACIÓN DE CADÁVER "

        elements = []
        styles = getSampleStyleSheet()

        elements.append(self.tabla_encabezado(styles))
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(self.tabla_fallecido(styles))
        elements.append(Spacer(1, 0 * cm))
        elements.append(self.tabla_dispone(styles))
        elements.append(Spacer(1, 1 * cm))
        elements.append(self.tabla_parrafo_fecha(styles))
        elements.append(Spacer(1, 12 * cm))
        elements.append(self.tabla_parrafo_pie_pagina(styles))
        elements.append(Spacer(1, 0 * cm))
        # SALTO DE PÁGINA -- >>
        elements.append(PageBreak())
        # SALTO DE PÁGINA -- >>
        elements.append(self.tabla_encabezado(styles))
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(self.tabla_numero_expediente(styles))
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(self.tabla_titulo_main(styles))
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(self.tabla_antecedentes_main(styles))
        elements.append(Spacer(1, 0))
        elements.append(self.tabla_body_estatico(styles))

        # doc.build(elements, canvasmaker=NumberedCanvas)
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
