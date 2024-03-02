# -*- coding: utf-8 -*-
from django.db import models

from apps.localizations.models.department import Department


class Province(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, related_name='provinces', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
