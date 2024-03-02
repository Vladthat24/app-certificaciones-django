import os
import sys

from apps.localizations.models.district import District

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass

from django.db import models
from django.utils.translation import gettext_lazy as _


class Hospital(models.Model):
    institucion = models.CharField(_('Institución'), max_length=250, null=True, blank=True)
    codigo_unico = models.CharField(_('Código Único'), max_length=8, null=True, blank=True)
    nombre_establecimiento = models.TextField(_('Nombre del establecimiento'), max_length=500)
    clasificacion = models.TextField(_('Clasificación'), max_length=250, null=True, blank=True)
    tipo = models.TextField(_('Tipo'), max_length=250, null=True, blank=True)
    distrito = models.ForeignKey(District, verbose_name='Distrito', on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.TextField(_('Dirección'), max_length=550, null=True, blank=True)

    codigo_disa = models.CharField(_('Código DISA'), max_length=2, null=True, blank=True)
    codigo_red = models.CharField(_('Código Red'), max_length=2, null=True, blank=True)
    codigo_microred = models.CharField(_('Código Microred'), max_length=2, null=True, blank=True)
    disa = models.CharField(_('DISA'), max_length=150, null=True, blank=True)
    red = models.CharField(_('Red'), max_length=150, null=True, blank=True)
    microred = models.CharField(_('Microred'), max_length=150, null=True, blank=True)
    categoria = models.CharField(_('Categoría'), max_length=150, null=True, blank=True)
    telefono = models.CharField(_('Categoría'), max_length=150, null=True, blank=True)
    director = models.CharField(_('Director'), max_length=250, null=True, blank=True)
    estado = models.CharField(_('Estado'), max_length=15, null=True, blank=True)
    norte = models.CharField(_('Norte'), max_length=15, null=True, blank=True)
    este = models.CharField(_('Este'), max_length=15, null=True, blank=True)
    ruc = models.CharField(_('Ruc'), max_length=11, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Hospital')
        verbose_name_plural = _('Hospitales')

    @property
    def get_ubicacion(self):
        if self.distrito:
            return "%s - %s -%s " % (
                self.distrito.province.department.name, self.distrito.province.name, self.distrito.name)

    def __str__(self):
        return "%s, %s, %s " % (self.codigo_unico, self.nombre_establecimiento, self.direccion)
