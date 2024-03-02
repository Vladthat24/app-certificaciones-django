# if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
#     import django

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.middlewares.request import AppRequestMiddleware
from apps.solicitud.models.solicitud import Solicitud
from apps.util.network import get_client_ip

TIPOS = (
    (1, 'CREMACIÓN'),
    (2, 'INHUMACIÓN'),
    (3, 'TRASLADO'),
    (4, 'EXHUMACIÓN Y TRASLADO DE RESTOS HUMANOS'),
    (5, 'EXHUMACIÓN, TRASLADO Y CREMACIÓN DE RESTOS HUMANOS'),
    (6, 'OTROS'),
)


class Certificacion(models.Model):
    solicitud = models.OneToOneField(Solicitud, verbose_name="Solicitud", on_delete=models.CASCADE, null=True,
                                     blank=True)
    numero_autorizacion = models.CharField(_('Número de autorización'), max_length=15)
    # numero_expediente = models.CharField(_('Número de expediente'), max_length=15, null=True, blank=True)
    # fecha_recepcion = models.DateField(_('Fecha de recepción por mesa de partes virtual'), null=True, blank=True)
    motivo = models.TextField(_('Motivo'), max_length=3000)
    tipo = models.PositiveIntegerField(_('Tipo de autorización'), choices=TIPOS, default=1)
    tipo_otro = models.TextField(_('Otros'), max_length=500, null=True, blank=True)
    orden = models.PositiveIntegerField(_('Orden'), default=1)

    solicitante_dni = models.CharField(_('Solicitante DNI'), max_length=12, null=True, blank=True)
    solicitante = models.TextField(_('Solicitante'), max_length=350, null=True, blank=True)
    parentesco = models.CharField(_('Parentesco Fallecido'), max_length=150, null=True, blank=True)
    parentesco_solicitante = models.CharField(_('Parentesco Solicitante'), max_length=150, null=True, blank=True)
    fallecido_dni = models.CharField(_('Fallecido DNI'), max_length=12, null=True, blank=True)
    fallecido_nombre = models.TextField(_('Nombre Fallecido'), max_length=350, null=True, blank=True)
    fallecido_fecha = models.DateField(_('Fecha de fallecimiento'), null=True, blank=True)
    fallecido_hora = models.CharField('hora de fallecimiento', max_length=15, null=True, blank=True)
    fallecido_direccion = models.TextField(_('Dirección fallecimiento'), max_length=1500, null=True, blank=True)
    necropsia_causa_muerte = models.TextField(_('Causa de muerte según necropsia'), max_length=1500, null=True,
                                              blank=True)
    necropsia_numero = models.TextField(_('Nº de certificado y prod. de necropcia'), max_length=1500, null=True,
                                        blank=True)
    fecha_cert_necropsia = models.DateField(_('Fecha Cert. Necropsia'), max_length=1500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_ip = models.CharField(max_length=20, null=True, blank=True)
    updated_ip = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = _('Certificación')
        verbose_name_plural = _('Certificaciones')
        ordering = ['-orden']

    def __str__(self):
        return "%s - %s  - %s" % (self.solicitud, str(self.numero_autorizacion), str(self.orden))

    def save(self, *args, **kwargs):
        current_request = AppRequestMiddleware.get_request()
        if len(self.numero_autorizacion.split("-")) > 0:
            self.orden = int(self.numero_autorizacion.split("-")[0])
        else:
            self.orden = int(self.numero_autorizacion)

        try:
            if self._state.adding:
                solicitud = Solicitud.objects.get(pk=self.solicitud.pk)
                solicitud.estado = 4
                solicitud.save()
                # self.created_by = u
                # self.updated_by = u
                self.created_ip = get_client_ip(current_request)
                self.updated_ip = get_client_ip(current_request)
            else:
                self.updated_ip = get_client_ip(current_request)
                # self.updated_by = u
        except KeyError:
            self.updated_ip = get_client_ip(current_request)
            # self.updated_by = u
        super(Certificacion, self).save(*args, **kwargs)
