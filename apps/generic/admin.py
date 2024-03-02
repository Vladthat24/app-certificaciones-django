from django.contrib import admin

from apps.generic.models.anio import Anio
from apps.generic.models.rango_horario import RangoHorario
from apps.generic.models.resolucion import Resolucion






#admin.site.register(Resolucion)
admin.site.register(Anio)
admin.site.register(RangoHorario)


@admin.register(Resolucion)
class ResolucionAdmin(admin.ModelAdmin):
    search_fields = ('nombre_director',)
    list_filter = ('nombre_director',)
    list_display = ('nombre_director', 'resolucion', 'estado', 'created_at')
