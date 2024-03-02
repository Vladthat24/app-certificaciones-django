from django.contrib import admin

from apps.certificacion.models.certificacion import Certificacion
from apps.generic.models.calendario_feriado import CalendarioFeriado


class CertificacionAdmin(admin.ModelAdmin):
    """docstring for UserAdmin"""
    ordering = ['-id']
    search_fields = (
        'numero_autorizacion', 'solicitud__fallecido_nombres', 'solicitud__fallecido_apellido_paterno',
        'solicitud__fallecido_apellido_materno', 'solicitud__fallecido_numero_documento',
        'solicitud__solicitante_numero_documento')
    list_display = (
        'numero_autorizacion', 'created_at', 'get_solicitud')

    def get_solicitud(self, obj):
        if obj.solicitud:
            # return str(
            #     obj.solicitud.fallecido_nombres + " - " + obj.solicitud.fallecido_apellido_paterno + " - "
            #     + obj.solicitud.fallecido_apellido_materno + " - " + obj.solicitud.fallecido_numero_documento)
            return "CON  SOLICITUD"
        else:
            return "SIN SOLICITUD"

    get_solicitud.admin_order_field = 'id'  # Allows column order sorting
    get_solicitud.short_description = 'SOLICITUD'  # Renames column head


class DistrictAdmin(admin.ModelAdmin):
    search_fields = ('code', 'name',)


admin.site.register(Certificacion, CertificacionAdmin)

admin.site.register(CalendarioFeriado)
