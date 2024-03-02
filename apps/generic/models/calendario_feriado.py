from django.db import models
from django.utils.translation import gettext_lazy as _

TIPOS = (
    (1, 'FERIADO CALENDARIO'),
    (2, 'FERIADO NACIONAL'),
    (3, 'OTROS'),
)


class CalendarioFeriado(models.Model):
    title = models.CharField(_('Título'), max_length=250, default='No Laborable')
    date = models.DateField(_('Fecha'), unique=True)
    type = models.IntegerField(_('Tipo'), choices=TIPOS, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Calendario Feriado')
        verbose_name_plural = _('Calendario Feriado')

    def __str__(self):
        return "%s, %s" % (self.title, self.date)
