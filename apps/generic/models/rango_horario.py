from django.db import models
from django.utils.translation import gettext_lazy as _


class RangoHorario(models.Model):
    rango = models.TimeField(_('Hora límite'))
    state = models.BooleanField(_('Estado'), default=False)

    class Meta:
        verbose_name = _('Rango Harario')
        verbose_name_plural = _('Rangos horarios')

    def save(self, *args, **kwargs):
        if self.state:
            RangoHorario.objects.filter(state=True).update(state=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return "%s, %s" % (self.rango, self.state)
