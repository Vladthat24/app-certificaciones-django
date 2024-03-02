import os
import sys

import django

# django.setup()

from django.db import models

class Periodo(models.Model):
    periodo = models.CharField('periodo', unique=True, max_length=80)
    fecha_inicio = models.DateField('Fecha de incio')
    fecha_fin = models.DateField('Fecha de fin')
    estado = models.BooleanField('Estado', max_length=30, default=True)

    def __str__(self):
        return " %s " % (self.periodo)

    def save(self, *args, **kwargs):
        if self.estado:
            Periodo.objects.all().update(estado=False)
        super(Periodo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
