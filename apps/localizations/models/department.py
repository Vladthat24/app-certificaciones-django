from django.db import models

from apps.localizations.models.country import Country


class Department(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=250)
    country = models.ForeignKey(Country, related_name='departments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

