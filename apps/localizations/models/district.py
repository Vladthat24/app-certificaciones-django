from django.db import models

from apps.localizations.models.province import Province


class District(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=150)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    province = models.ForeignKey(Province, related_name='districts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    def get_full_name(self):
        return "%s - %s - %s" % (
            self.province.department.name, self.province.name, self.name)
