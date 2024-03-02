import os
import sys

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

TYPES = (
    (0, 'PERFIL_PACIENTE'),
    (1, 'ADMINISTRADOR'),
)


class Menu(models.Model):
    name = models.CharField(_('nombre'), max_length=30)
    icon = models.CharField(_('icono'), max_length=30, default="home")
    url = models.CharField(_('url'), max_length=80)
    title = models.CharField(_('título'), max_length=30, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='childrens', null=True, blank=True, on_delete=models.CASCADE)
    type = models.IntegerField(_('tipo'), choices=TYPES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')


class GroupMenu(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)
    menus = models.ManyToManyField(Menu, verbose_name=_('grupos menus'),
                                   blank=True,
                                   help_text=_('Especifica los menus del grupo.'), )

    def __str__(self):
        return self.group.name

    class Meta:
        verbose_name = _('Grupo Menu')
        verbose_name_plural = _('Grupo Menus')
