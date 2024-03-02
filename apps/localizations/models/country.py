# import os
# import sys
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
#
# if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
#     import django
#     django.setup()

from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    code = models.CharField(_('Código'), max_length=5)
    name = models.CharField(_('Nombre'), max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('País')
        verbose_name_plural = _('Países')
