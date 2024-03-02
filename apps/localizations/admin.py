from django.contrib import admin

from apps.localizations.models.country import Country
from apps.localizations.models.department import Department
from apps.localizations.models.district import District
from apps.localizations.models.province import Province


class DistrictProvince(admin.ModelAdmin):
    search_fields = ('code', 'name',)


class DistrictAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name',)


admin.site.register(Country)
admin.site.register(Department)
admin.site.register(Province, DistrictProvince)
admin.site.register(District, DistrictAdmin)
