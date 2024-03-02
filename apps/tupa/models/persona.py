from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.solicitud.models.solicitud import TIPOS_DOCUMENTO, ESTADOS_CIVILES


class Persona(models.Model):
    tipo_documento = models.PositiveIntegerField(_('Tipo de documento'), choices=TIPOS_DOCUMENTO, default=1)
    numero_documento = models.CharField(_('Número de documento'), max_length=12, null=True, blank=True)
    nombres = models.CharField(_('Nombres'), max_length=150, null=True, blank=True)
    apellido_paterno = models.CharField(_('Apellido paterno'), max_length=150, null=True, blank=True)
    apellido_materno = models.CharField(_('Apellido materno'), max_length=150, null=True, blank=True)
    estado_civil = models.PositiveIntegerField(_('Estado civil'), choices=ESTADOS_CIVILES, null=True, blank=True)
    solicitante_direccion = models.TextField(_('Domicilio'), max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')

    def __str__(self):
        return "%s - %s %s %s " % (
            self.numero_documento, self.nombres, self.apellido_paterno, self.apellido_materno)
