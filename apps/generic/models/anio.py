from django.db import models
from django.utils.translation import gettext_lazy as _


class Anio(models.Model):
    nombre = models.CharField('Nombre', max_length=350)
    state = models.BooleanField('Estado', default=True)

    class Meta:
        verbose_name = _('Año')
        verbose_name_plural = _('Años')
        ordering = ["-nombre"]

    def save(self, *args, **kwargs):
        if self.state:
            Anio.objects.filter(state=True).update(state=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return "%s - %s" % (self.nombre, self.state)
