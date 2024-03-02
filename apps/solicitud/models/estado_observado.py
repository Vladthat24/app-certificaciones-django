import os
import sys

from apps.middlewares.request import AppRequestMiddleware
from apps.solicitud.models.solicitud import Solicitud
from apps.util.network import get_client_ip
from setup.models.usuario import Usuario

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass

from django.db import models
from django.utils.translation import gettext_lazy as _

ESTADOS_OBSERVACION = (
    (1, 'OBSERVADO'),
    (2, 'CORREGIDO'),
)


class EstadoObservado(models.Model):
    solicitud = models.ForeignKey(Solicitud, verbose_name='Solicitud', on_delete=models.CASCADE, related_name="estados")
    observacion = models.TextField(_("Observación"), max_length=3000)
    descargo = models.TextField(_("Descargo"), max_length=3000, null=True, blank=True)
    estado = models.PositiveIntegerField(_("Estado"), choices=ESTADOS_OBSERVACION, default=1)
    observacion_archivo = models.FileField(_("Observacion archivo"), null=True, blank=True)
    descargo_archivo = models.FileField(_("Descargo archivo"), null=True, blank=True)
    created_ip = models.CharField(max_length=20, null=True, blank=True)
    updated_ip = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Usuario, related_name='users_created_estados', null=True, blank=True,
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(Usuario, related_name='users_updated_estados', null=True, blank=True,
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Estado Observado')
        verbose_name_plural = _('Estado Observado')

    def __str__(self):
        return "%s, %s, %s " % (
            self.solicitud.solicitante_numero_documento, self.observacion, self.get_estado_display())

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

        super(EstadoObservado, self).save(*args, **kwargs)
