from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.tupa.models.persona import Persona
from setup.models.usuario import Usuario


class Solicitante(Persona):
    correo = models.EmailField(_('Correo'))
    celular = models.CharField(_('Celular'), max_length=11)
    usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Solicitante')
        verbose_name_plural = _('Solicitantes')

    def __str__(self):
        return "%s - %s %s %s " % (
            self.numero_documento, self.nombres, self.apellido_paterno, self.apellido_materno)
