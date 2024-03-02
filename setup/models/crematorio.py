import os
import sys

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.localizations.models.district import District

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass


class Crematorio(models.Model):
    direccion = models.TextField(_('direccion'), max_length=800)
    nombre = models.TextField(_('nombre'), max_length=300)
    distrito = models.ForeignKey(District, verbose_name="Distrito", on_delete=models.CASCADE)
    estado = models.BooleanField(_('Estado'), default=True)

    def __str__(self):
        return " %s  %s " % (self.nombre, self.direccion)

    class Meta:
        verbose_name = _('Crematorio')
        verbose_name_plural = _('Crematorio')
