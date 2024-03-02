import os
import sys
from datetime import datetime

from apps.localizations.models.district import District
from apps.middlewares.request import AppRequestMiddleware
from apps.solicitud.models.hospital import Hospital
from apps.solicitud.util import get_fecha_excluyendo_no_laborables
from apps.util.network import get_client_ip
from setup.models.crematorio import Crematorio
from setup.models.usuario import SEXS, Usuario

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass

from django.db import models
from django.utils.translation import gettext_lazy as _

PARENTESCO = (
    (1, 'Madre'),
    (2, 'Padre'),
    (3, 'Hijo'),
    (4, 'Hija'),
    (5, 'Hermano'),
    (6, 'Hermana'),
    (7, 'Cónyuge'),
    (8, 'Óbito fetal'),

    (9, 'Abuelo'),
    (10, 'Abuela'),

    (11, 'Tío'),
    (12, 'Tía'),

    (13, 'Nieto'),
    (14, 'Nieta'),

    (15, 'Sobrino'),
    (16, 'Sobrina'),

    (17, 'Primo'),
    (18, 'Prima'),
)

TIPOS_SOLICITUD = (
    (1, 'Cremación'),
    (2, 'Traslado'),
    (3, 'Inhumado'),
    (4, 'Inhumado en el cementerio')
)

TIPOS_DOCUMENTO = (
    (1, 'D.N.I.'),
    (2, 'Carné de extrangería'),
    (3, 'Pasaporte'),
    (4, 'NN'),
    (5, 'A.S.'),
    (6, 'C.I.'),
    (7, 'P.T.P.'),
    (8, 'Acta de nacimiento'),
)

ESTADOS_CIVILES = (
    (1, 'Soltero(a)'),
    (2, 'Casado(a)'),
    (3, 'Viudo(a)'),
    (4, 'Divorciado(a)'),
)

LUGAR_FALLECIMIENTO = (
    (1, 'Hospital'),
    (2, 'Domicilio'),
    (3, 'Vía pública'),
    (4, 'Otros'),
)

# estado de autorizacion
ESTADOS = (
    (1, 'Pendiente'),
    (2, 'Registrado'),
    (3, 'Observado'),
    (4, 'Autorizado'),
    (5, 'Certificado'),
)

ESTADOS_OBSERVADO_SOLICITUD = (
    (0, 'Sin observaciones'),
    (1, 'Observado'),
    (2, 'Corregido'),
)


class Solicitud(models.Model):
    crematorio = models.ForeignKey(Crematorio, verbose_name="Crematorio", on_delete=models.CASCADE, null=True,
                                   blank=True)
    tipo = models.PositiveIntegerField(_('Tipo de solicitud'), choices=TIPOS_SOLICITUD, default=1)
    """
    DATOS DEL SOLICITANTE
    """
    solicitante_tipo_documento = models.PositiveIntegerField(_('Tipo de documento'), choices=TIPOS_DOCUMENTO, default=1)
    solicitante_numero_documento = models.CharField(_('Número de documento'), max_length=12, null=True, blank=True)
    solicitante_nombres = models.CharField(_('Nombres'), max_length=150, null=True, blank=True)
    solicitante_apellido_paterno = models.CharField(_('Apellido paterno'), max_length=150, null=True, blank=True)
    solicitante_apellido_materno = models.CharField(_('Apellido materno'), max_length=150, null=True, blank=True)
    solicitante_estado_civil = models.PositiveIntegerField(_('Estado civil'), choices=ESTADOS_CIVILES, null=True,
                                                           blank=True)
    solicitante_correo = models.EmailField(_('Correo'), null=True, blank=True)
    solicitante_celular = models.CharField(_('Celular'), max_length=12, null=True, blank=True)
    solicitante_parentesco = models.PositiveIntegerField(_('Parentesco'), choices=PARENTESCO, null=True, blank=True)
    # solicitante_distrito = models.ForeignKey(District, verbose_name='Distrito', on_delete=models.CASCADE)
    solicitante_direccion = models.TextField(_('Domicilio'), max_length=800, null=True, blank=True)
    solicitante_departamento_name = models.CharField(_('Departamento'), max_length=300, null=True, blank=True)
    solicitante_provincia_name = models.CharField(_('Provincia'), max_length=300, null=True, blank=True)
    solicitante_distrito_name = models.CharField(_('Distrito'), max_length=300, null=True, blank=True)
    """
    DATOS DEL FALLECIDO
    """
    fallecido_tipo_documento = models.PositiveIntegerField(_('Tipo de documento'), choices=TIPOS_DOCUMENTO, default=1)
    fallecido_numero_documento = models.CharField(_('Número de documento'), max_length=12, null=True, blank=True)
    fallecido_nombres = models.CharField(_('Nombres'), max_length=150, null=True, blank=True)
    fallecido_apellido_paterno = models.CharField(_('Apellido paterno'), max_length=150, null=True, blank=True)
    fallecido_apellido_materno = models.CharField(_('Apellido materno'), max_length=150, null=True, blank=True)
    fallecido_sexo = models.PositiveIntegerField(_('Género'), choices=SEXS, default=1, null=True, blank=True)
    fallecido_fecha_nacimiento = models.DateField(_('Fecha de nacimiento'), null=True, blank=True)
    fallecido_estado_civil = models.PositiveIntegerField(_('Estado civil'), choices=ESTADOS_CIVILES, null=True,
                                                         blank=True)
    fallecido_fecha_fallecimiento = models.DateField(_('Fecha de fallecimiento'))
    fallecido_hora_fallecimiento = models.CharField('hora de fallecimiento', max_length=15)
    fallecido_parentesco = models.PositiveIntegerField(_('Parentesco con el solicitante'), choices=PARENTESCO,
                                                       null=True, blank=True)

    """
    LUGAR DEL FALLECIMIENTO
    """
    lugar_fallecimiento_tipo = models.PositiveIntegerField(_('Lugar'), choices=LUGAR_FALLECIMIENTO, default=1)
    lugar_fallecimiento_preposicion_titulo = models.CharField(_('Preposición título (Falleció..)'), max_length=30,
                                                              null=True, blank=True)
    lugar_fallecimiento_hospital = models.ForeignKey(Hospital, verbose_name="Hospital", on_delete=models.CASCADE,
                                                     null=True, blank=True)
    hospital_id = models.IntegerField(_('Hospital id - Para validar'), default=0)
    lugar_fallecimiento_direccion = models.TextField(_('Dirección'), max_length=800, null=True, blank=True)
    lugar_fallecimiento_distrito = models.ForeignKey(District, verbose_name='Distrito', on_delete=models.CASCADE,
                                                     related_name="fallecimiento_distrito", null=True, blank=True)

    """
    ARCHIVO ADJUNTO
    """

    archivo = models.FileField(_('Archivo adjunto PDF (Max. 5Mb)'), null=True, blank=True)
    fecha_cremacion = models.DateField(_('Fecha de cremación'))
    hora_cremacion = models.CharField('hora de cremación', max_length=15, null=True, blank=True)
    estado = models.PositiveIntegerField(_('Estado'), choices=ESTADOS, default=1)

    numero_expediente = models.CharField(_('Número de expediente'), null=True, blank=True, max_length=50)

    # estado_solicitud_obs = models.TextField(_('Observacion'), max_length=1000, null=True, blank=True)

    constancia_deposito = models.FileField(_('Constancia de depósito (Max. 5Mb)'), null=True, blank=True)
    tesoreria_valid = models.BooleanField(default=False)

    """
        Fecha que se guarda en Mesa de partes cuando registra el número de expediente
    """
    registrado_fecha = models.DateTimeField(null=True, blank=True)

    """
    Comprobante de pago subido por DSAIA
    """
    comprobante = models.FileField(_('Comprobante de pago subido por DSAIA'), null=True, blank=True)

    """
    Archivo escaneado
    """
    escaneado = models.FileField(_('Escaneado'), null=True, blank=True)
    es_covid = models.BooleanField(_('- ¿ Covid ?'))
    numero_deposito = models.CharField(_('Número de depósito'), max_length=100)

    """
    Estado observado de la solicitud
    """
    estado_observado = models.IntegerField(_("Estado observado"), choices=ESTADOS_OBSERVADO_SOLICITUD, default=0)

    """
    Fecha de envío cuando el crematorio ingresa los dos documentos escaneados, (Constancia de pago y la solicitud escaneada y firmada)
    """

    fecha_envio = models.DateTimeField(null=True, blank=True)

    """
        21/06/2021
    """

    numero_necropsia = models.CharField(_('Número de necropsia'), null=True, blank=True, max_length=50)
    fecha_necropsia = models.DateField(_('Fecha de necropsia'), null=True, blank=True)

    fecha_deposito = models.DateField(_('Fecha de deposito'))
    destino_cenizas = models.TextField(_('Destino final de cenizas'), max_length=700)

    " 30/06/2022"

    created_ip = models.CharField(max_length=20, null=True, blank=True)
    updated_ip = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, related_name='created', null=True, blank=True,
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(Usuario, related_name='updated', null=True, blank=True,
                                   on_delete=models.CASCADE)

    """
          Fecha que se guarda en la que valida mesa de partes.
    """
    validacion_tesoreria_fecha = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Solicitud')
        verbose_name_plural = _('Solicitudes')

    def save(self, *args, **kwargs):

        # Auditoria
        current_request = AppRequestMiddleware.get_request()
        u = current_request.user
        if self.pk:
            self.updated_ip = get_client_ip(current_request)
            if not u.is_anonymous:
                self.updated_by = u
        else:
            if not u.is_anonymous:
                self.created_by = u
                self.updated_by = u
            self.created_ip = get_client_ip(current_request)
            self.updated_ip = get_client_ip(current_request)



        if self._state.adding:
            self.estado = 1
            self.pendiente_fecha = datetime.now()

        else:

            # if self.tesoreria_valid and not self.validacion_tesoreria_fecha:
            #     self.validacion_tesoreria_fecha = datetime.now()

            if self.archivo and self.constancia_deposito:
                if not self.fecha_envio:
                    # self.fecha_envio = datetime.now()
                    self.fecha_envio = get_fecha_excluyendo_no_laborables()

            if self.estado_observado > 0:
                instance = Solicitud.objects.get(pk=self.pk)
                self.archivo = instance.archivo
                self.constancia_deposito = instance.constancia_deposito

        super(Solicitud, self).save(*args, **kwargs)

    def __str__(self):
        return self.fallecido_numero_documento if self.fallecido_numero_documento else "-"

    def get_solicitante(self):
        if self.solicitante_apellido_paterno:
            return (self.solicitante_nombres if self.solicitante_nombres else ".") + " " + \
                   (self.solicitante_apellido_paterno if self.solicitante_apellido_paterno else ".") + " " + \
                   (self.solicitante_apellido_materno if self.solicitante_apellido_materno else ".")
        else:
            return "AUTORIDAD SANITARIA"

    def get_fallecido(self):
        if self.fallecido_nombres and self.fallecido_apellido_paterno and self.fallecido_apellido_materno:
            return self.fallecido_nombres + " " + self.fallecido_apellido_paterno + " " + self.fallecido_apellido_materno
        return "NN"

    def get_hospital_nombre(self):
        if self.lugar_fallecimiento_hospital:
            nombre = str(self.lugar_fallecimiento_hospital.nombre_establecimiento)
            if nombre.split(" ")[0].casefold() == "HOSPITAL".casefold():
                nombre = nombre.replace('HOSPITAL ', '')
                nombre = nombre.replace('Hospital ', '')
                nombre = nombre.replace('hospital ', '')
            return nombre
            # return self.lugar_fallecimiento_hospital.nombre_establecimiento
        else:
            return ""

    def get_direccion_fallecimiento(self):

        if self.lugar_fallecimiento_hospital:
            dict_return = {
                "direccion": self.lugar_fallecimiento_hospital.direccion,
                "distrito": self.lugar_fallecimiento_hospital.distrito.name,
                "provincia": self.lugar_fallecimiento_hospital.distrito.province.name,
                "departamento": self.lugar_fallecimiento_hospital.distrito.province.department.name,
                "distrito_id": self.lugar_fallecimiento_hospital.distrito.id,
                "provincia_id": self.lugar_fallecimiento_hospital.distrito.province.id,
            }
        else:
            dict_return = {
                "direccion": self.lugar_fallecimiento_direccion,
                "distrito": self.lugar_fallecimiento_distrito.name,
                "provincia": self.lugar_fallecimiento_distrito.province.name,
                "departamento": self.lugar_fallecimiento_distrito.province.department.name,
                "distrito_id": self.lugar_fallecimiento_distrito.id,
                "provincia_id": self.lugar_fallecimiento_distrito.province.id,
            }

        return dict_return

    def get_certificado(self):
        from apps.certificacion.models.certificacion import Certificacion
        try:
            return Certificacion.objects.get(solicitud_id=self.id)
        except Certificacion.DoesNotExist:
            return False

    def get_estado_observado(self):
        from apps.solicitud.models.estado_observado import EstadoObservado
        result = 0
        if len(self.estados.all()) > 0:
            result = 2
        try:
            if self.estados.last().estado == 1:
                result = 1
        except EstadoObservado.DoesNotExist:
            pass
            # if len(self.estados.filter(estado=1)) > 0:
            #     result = 1
        return result

    def get_estado_observado_oficina(self):

        estado = {"estado_solicitud": 0, "estado_observado": 0}
        current_request = AppRequestMiddleware.get_request()
        u = current_request.user
        if not u.is_anonymous:
            ultimo_estado = self.estados.filter(created_by=u).last()
            if ultimo_estado:
                estado["estado_observado"] = ultimo_estado.estado

        return estado


    def get_fecha_certificado(self):
        from apps.certificacion.models.certificacion import Certificacion
        try:
            return Certificacion.objects.get(solicitud_id=self.id).created_at
        except Certificacion.DoesNotExist:
            return "-"