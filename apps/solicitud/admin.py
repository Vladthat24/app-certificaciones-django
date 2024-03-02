from django.contrib import admin

from apps.load_excel.read_only import run_file_hospital
from apps.solicitud.models.estado_observado import EstadoObservado
from apps.solicitud.models.hospital import Hospital
from apps.solicitud.models.solicitud import Solicitud


class HospitalAdmin(admin.ModelAdmin):
    """docstring for UserAdmin"""
    ordering = ['-id']
    search_fields = ('codigo_unico', 'nombre_establecimiento')

    # actions = ['run_excel']

    def run_excel(self, request, queryset):
        run_file_hospital()
        # prueba_dni()


class SolicitudAdmin(admin.ModelAdmin):
    """docstring for UserAdmin"""
    ordering = ['-id']
    search_fields = (
        'fallecido_nombres', 'fallecido_apellido_paterno', 'fallecido_apellido_materno', 'fallecido_numero_documento',
        'numero_expediente')
    list_display = (
        'numero_expediente','fallecido_fecha_fallecimiento', 'registrado_fecha', 'fallecido_nombres', 'fallecido_apellido_paterno',
        'fallecido_apellido_materno', 'fallecido_numero_documento',
        'created_at', 'crematorio',)
    readonly_fields = ('created_at', 'updated_at', 'created_ip', 'updated_ip', 'created_by', 'updated_by', 'crematorio')


admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Hospital, HospitalAdmin)


@admin.register(EstadoObservado)
class PetAdmin(admin.ModelAdmin):
    list_display = ('estado', 'created_at', 'updated_at', 'get_solicitud',)
    search_fields = ('solicitud__solicitante_numero_documento', 'solicitud__fallecido_numero_documento')

    def get_solicitud(self, obj):
        return "%s, %s - %s" % (obj.solicitud.solicitante_nombres, obj.solicitud.solicitante_numero_documento,
                                obj.solicitud.fallecido_numero_documento)

    get_solicitud.short_description = 'Solicitud'
    get_solicitud.admin_order_field = 'solicitud_id'
