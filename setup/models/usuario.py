import os
import sys

from setup.models.crematorio import Crematorio

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    import django

    django.setup()

from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from setup.models.entidad import Entidad

TYPES = (
    ('DNI', 'DNI'),
    ('PASSPORD', 'PASAPORTE'),
)

DEGRESS = (
    (0, 'SIN ESTUDIOS'),
    (1, 'PRIMARIA COMPLETA'),
    (2, 'PRIMARIA INCOMPLETA '),
    (3, 'SECUNDARIA COMPLETA'),
    (4, 'SECUNDARIA INCOMPLETA'),
    (5, 'ESTUDIOS SUPERIORES'),
)

CIVIL_STATUS = (
    (1, 'SOLTERO'),
    (2, 'CASADO'),
    (3, 'VIUDO'),
    (4, 'DIVORCIADO'),
)

SEXS = (
    (1, 'MASCULINO'),
    (2, 'FEMENINO'),
)

RIS = (
    (0, ' ----------'),
    (1, 'RIS BCO-CHO-SCO'),
    (2, 'RIS LURIN Y BALNERARIOS'),
    (3, 'RIS PACHACAMAC'),
    (4, 'RIS SJM'),
    (5, 'RIS VES'),
    (6, 'RIS VMT'),
    (7, 'DIRIS SEDE ADMINISTRATIVA'),
)


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class Usuario(AbstractUser):
    entidad = models.ForeignKey(Entidad, verbose_name='IPRESS', on_delete=models.CASCADE, null=True, blank=True)
    # document = models.CharField(_('número de DNI'), max_length=12, unique=True, validators=[
    #     RegexValidator(regex='^.{8}$', message=_('Tiene que ingresa 8 dígitos'), code='nomatch')])

    document = models.CharField(_('número de DNI'), max_length=12, null=True, blank=True)
    celular = models.IntegerField(_('número de celular'), null=True, blank=True, validators=[
        RegexValidator(regex='^.{9}$', message=_('tiene que ingresa 9 dígitos.'), code='nomatch')])

    ris = models.IntegerField(_('Administrador RIS'), choices=RIS, default=0)

    crematorio = models.ForeignKey(Crematorio, verbose_name='Crematorio', on_delete=models.CASCADE, null=True,
                                   blank=True)

    # document = models.CharField(_('número de DNI'), max_length=12, unique=True, validators=[
    #     RegexValidator(regex='^.{8}$', message=_('Tiene que ingresa 8 dígitos'), code='nomatch')])

    # REQUIRED_FIELDS = ['entidad']

    # renipress = models.CharField(_('Renipress'), max_length=25, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
