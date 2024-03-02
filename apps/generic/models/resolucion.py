from django.db import models
from django.utils.translation import gettext_lazy as _


class Resolucion(models.Model):
    nombre_director = models.CharField(_('Nombre director'), max_length=250, null=True, blank=True)
    resolucion = models.CharField(_('Resolución'), max_length=30, null=True, blank=True)
    estado = models.BooleanField(_('Estado'), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Resolución')
        verbose_name_plural = _('Resolución')

    def __str__(self):
        return "%s, %s" % (self.nombre_director, self.resolucion)
