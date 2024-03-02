import os
import sys

from apps.certificacion.models.certificacion import Certificacion
from apps.certificacion.views.report_pdf_certificacion_autoridad_sanitaria import ReportCertificadoAutoridadSanitaria
from apps.certificacion.views.report_pdf_certificacion_obito import ReportCertificadoObito
from apps.generic.models.resolucion import Resolucion
from apps.certificacion.views.report_util import *

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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, TableStyle, PageBreak
from reportlab.platypus import Table
from reportlab.platypus.flowables import Spacer

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm, inch, mm
from reportlab.pdfgen import canvas

import locale

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


class ReportCertificadoNoCovid():
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

      #if solicitante_sexo == 1:
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
            + " por la oficina de Trámite Documentario de la DIRIS Lima Sur, presentado por "+self.tenor_solicitante
            + " <font name='Calibri-Bold' size='12'>" + self.certificado.solicitud.get_solicitante() + "</font>, y; ",
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
            u"Que, mediante el documento de la referencia, <font name='Calibri-Bold' size='11'>" +
            self.certificado.solicitud.get_solicitante() + "</font>, solicita la autorización sanitaria"
            + " para la cremación del cadáver de su " + self.certificado.solicitud.get_fallecido_parentesco_display() + ", "
            + "<font name='Calibri-Bold' size='11'>" + self.certificado.solicitud.get_fallecido() + "</font>, "
            +self.valor_fallecido+ " el día " + self.certificado.solicitud.fallecido_fecha_fallecimiento.strftime(
                "%d de %B del %Y") + ", "
            + preposicion_titulo
            + nombre_hospital
            + " sito en " + self.certificado.fallecido_direccion + ", "
            + " del distrito de " + self.certificado.solicitud.get_direccion_fallecimiento()["distrito"] + ", "
            + distrito_name
            + "siendo la causa de muerte: <font name='Calibri-Bold' size='11'>"
            + self.certificado.motivo + "</font>, "
            + "según consta en el Certificado de Defunción obrante en el expediente; adjuntando además los documentos el Certificado de protocolo de "
              "necropsia y el certificado de embalsamamiento de acuerdo a la naturaleza del procedimiento.",
            sp_justifi_title_table)

        encabezado = [[titulo_antecedentes], [titulo_presenta]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_body_estatico(self, styles):

        parrafo_uno = Paragraph(
            u"Que, mediante Decreto Supremo N° 001-2016-SA, publicado en el Diario Oficial “El Peruano”, el 08 de enero de 2016, se aprobó el Texto Único de Procedimientos Administrativos (TUPA) del Ministerio de Salud y sus Órganos Desconcentrados, la misma que fue modificada mediante Resolución Ministerial N° 041-2018/MINSA, la cual señala taxativamente, - entre otros - los requisitos para acceder al otorgamiento de la  <font name='Calibri-Bold' size='11'> AUTORIZACIÓN SANITARIA PARA CREMACIÓN DE CADÁVER. </font>",
            sp_justifi_title_table)

        parrafo_uno_uno = Paragraph(
            u"Asimismo, de conformidad con el principio de legalidad, establecido en el Título Preliminar del T.U.O.  de la Ley N° 27444, Ley del Procedimiento Administrativo General, aprobado mediante Decreto Supremo N° 004-2019-JUS, se tiene que, las autoridades administrativas deben actuar con respeto a la Constitución, la ley y al derecho, dentro de las facultades que le estén atribuidas y de acuerdo con los fines para los que les fueron conferidas.",
            sp_justifi_title_table)

        parrafo_uno_dos = Paragraph(
            u"En ese sentido, la Ley N° 26842, Ley General de Salud, indica que la inhumación, exhumación, traslado y <font name='Calibri-Bold' size='11'>  cremación de cadáveres o restos humanos,</font>  así como el funcionamiento de cementerios y crematorios se rigen por las disposiciones de la ley de la materia y sus reglamentos.",
            sp_justifi_title_table)

        parrafo_uno_tres = Paragraph(
            u"En razón de ello, el artículo 21° de la Ley N° 26298, Ley General de Cementerios y Servicios Funerarios, establece que: <font name='Calibri-Bold' size='11'>  “Las cremaciones se efectuarán <u>previo cumplimiento</u> </font> de las disposiciones técnico-sanitarias <font name='Calibri-Bold' size='11'>y con autorización de la Autoridad de Salud,</font> salvo mandato judicial, de igual forma el artículo 24° de la misma norma de la materia, establece que: <font name='Calibri-Bold' size='11'>“Todo cadáver que haga posible la propagación de un daño a la salud humana, por la naturaleza de la enfermedad de la persona antes de morir, será cremado previa autorización de la Autoridad Sanitaria;</font>",
            sp_justifi_title_table)

        parrafo_tres = Paragraph(
            u"Que, los documentos obrantes en el expediente administrativo han sido presentados en copia simple por lo que de conformidad al principio de presunción de veracidad establecido en el numeral 1.7. del artículo IV del Título Preliminar del T.U.O. de la Ley N° 27444, Ley del Procedimiento Administrativo General, aprobado mediante Decreto Supremo N° 004-2019-JUS, los documentos y declaraciones formulados por los administrados responden a la verdad de los hechos que ellos afirman, reservándose la autoridad administrativa, el derecho de comprobar la veracidad de la información presentada de conformidad con el principio de privilegio de controles posteriores establecido en el numeral 1.16 del mismo artículo y norma administrativa descrita anteriormente.",
            sp_justifi_title_table)

        encabezado = [[parrafo_uno], [parrafo_uno_uno], [parrafo_uno_dos], [parrafo_uno_tres], [parrafo_tres]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle([]))
        return tabla_encabezado

    def tabla_body_estatico_uno(self, styles):

        resolucion = Resolucion.objects.filter(estado=True)
        resolucion_nombre = 'N° 287-2021-DIRIS-LS/DG'
        if len(resolucion) > 0:
            resolucion_nombre = resolucion[0].resolucion

        parrafo_cinco = Paragraph(
            u"Por lo expuesto, de conformidad con lo establecido en las normas y directivas de gestión de la materia y de conformidad a la Resolución Directoral " + resolucion_nombre + ", que designa a la suscrita como Directora Ejecutiva de la Dirección de Salud Ambiental e Inocuidad Alimentaria de la Dirección de Redes Integradas de Salud Lima Sur,<font name='Calibri-Bold' size='11'> SE RESUELVE:</font>",
            sp_justifi_title_table)

        encabezado = [[parrafo_cinco]]
        tabla_body = Table(encabezado)
        tabla_body.setStyle(TableStyle([]))
        return tabla_body

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
            u"<font name='Calibri-Bold' size='11'>AUTORIZAR</font> a "+self.tenor_solicitante+": <font name='Calibri-Bold' size='11'>" + self.certificado.solicitud.get_solicitante() + "</font>, "
            + self.valor_identificado_solicitante+ " con " + self.certificado.solicitud.get_solicitante_tipo_documento_display()
            + " N° " + self.certificado.solicitud.solicitante_numero_documento + ", "
            + " con eficacia anticipada al " + self.certificado.solicitud.fecha_cremacion.strftime(
                "%d de %B del %Y") + ", "
            + " para Cremar el Cadáver de su " + self.certificado.solicitud.get_fallecido_parentesco_display() + ", "
            + " <font name='Calibri-Bold' size='11'>" + self.certificado.solicitud.get_fallecido() + "</font>, "
            +self.valor_fallecido+ " el día " + self.certificado.solicitud.fallecido_fecha_fallecimiento.strftime(
                "%d de %B del %Y") + ", "
            + preposicion_titulo
            + nombre_hospital
            + " sito en " + self.certificado.fallecido_direccion + ", "
            + " del distrito de " + self.certificado.solicitud.get_direccion_fallecimiento()["distrito"] + ", "
            + distrito_name
            + " cuya causa de muerte fue: <font name='Calibri-Bold' size='11'>"
            + self.certificado.motivo + "</font>, "
            + " según consta en el Certificado de Defunción adjunto al presente, para ser incinerado en el Crematorio: "
            + self.certificado.solicitud.crematorio.nombre + ", sito en " + self.certificado.solicitud.crematorio.direccion +","
           + " del distrito de  " + self.certificado.solicitud.crematorio.distrito.name +","
           + "  provincia de " + self.certificado.solicitud.crematorio.distrito.province.name 
           + " y  departamento de " + self.certificado.solicitud.crematorio.distrito.province.department.name + ".",
            sp_justifi_title_table)



        encabezado = [[titulo_presenta]]
        tabla_encabezado = Table(encabezado)
        tabla_encabezado.setStyle(TableStyle(
            []
        ))
        return tabla_encabezado

    def tabla_dispone(self, styles):

        titulo_presenta = Paragraph(
            u"<font name='Calibri-Bold' size='12'>SE DISPONE: </font> Que, la Gerencia y/o Administración responsable del Crematorio, remita un Acta de Acreditación del procedimiento realizado debidamente firmada en un plazo máximo de diez (10) días útiles.",
            sp_justifi_title_table)

        encabezado = [[titulo_presenta]]
        tabla = Table(encabezado)
        tabla.setStyle(TableStyle(
            []
        ))
        return tabla

    # def tabla_exhorta(self, styles):
    #     titulo_presenta = Paragraph(
    #         u"<font name='Calibri-Bold' size='12'>SE EXHORTA: </font> A don(ña)"
    #         + " <font name='Calibri-Bold' size='11'>" + self.certificado.solicitud.get_solicitante() + "</font>, "
    #         + " que, al término del estado de emergencia cumpla con subsanar la documentación de acuerdo al "
    #         + "TUPA en virtud a lo establecido en la "
    #         + "<font name='Calibri-Italic' size='11'> “Directiva Sanitaria para el Manejo de Cadáveres por COVID - 19”</font>,"
    #         + " descrita en los párrafos precedentes.",
    #         sp_justifi_title_table)
    #
    #     encabezado = [[titulo_presenta]]
    #     tabla = Table(encabezado)
    #     tabla.setStyle(TableStyle(
    #         []
    #     ))
    #     return tabla

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
        elements.append(self.tabla_body_estatico_uno(styles))
        elements.append(Spacer(1, 0 * cm))
        elements.append(self.tabla_fallecido(styles))
        elements.append(Spacer(1, 0 * cm))
        elements.append(self.tabla_dispone(styles))
        elements.append(Spacer(1, 1 * cm))
        elements.append(self.tabla_parrafo_fecha(styles))
        elements.append(Spacer(1, 12 * cm))
        elements.append(self.tabla_parrafo_pie_pagina(styles))
        elements.append(Spacer(1, 0 * cm))

        # --->>> SALTO DE PAGINA
        elements.append(PageBreak())
        # --->>> SALTO DE PAGINA

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


def print_certificado_no_covid_pdf(request, pk):
    from django.http import HttpResponse
    response = HttpResponse(content_type='application/pdf')


    # Sexo: 1 - Masculino, 2: Femenino

    solicitante_sexo = 1
    try:
        certificado = Certificacion.objects.get(pk=pk)
        solicitante_sexo = get_sexo_solicitante(certificado)

    except Certificacion.DoesNotExist:
        certificado = Certificacion()


    if certificado.solicitud.solicitante_tipo_documento == 5:
        reporte = ReportCertificadoAutoridadSanitaria('A4', certificado,solicitante_sexo)
    else:
        if certificado.solicitud.fallecido_tipo_documento == 4:
            reporte = ReportCertificadoObito('A4', certificado,solicitante_sexo)
        else:
            reporte = ReportCertificadoNoCovid('A4', certificado,solicitante_sexo)

    pdf_name = "CERTIFICADO_" + str(certificado.numero_autorizacion).strip() + ".pdf"
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    pdf = reporte.imprimir()
    response.write(pdf)
    return response
