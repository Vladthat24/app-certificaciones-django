from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from apps.solicitud.models.estado_observado import EstadoObservado
from apps.solicitud.models.solicitud import Solicitud


class ListaEstadosSolicitud(TemplateView):
    template_name = "solicitud/estado_observaciones_list.html"

    def get_context_data(self, **kwargs):
        # update_project_session(self.request)
        context = super(ListaEstadosSolicitud, self).get_context_data(**kwargs)
        context['solicitud'] = Solicitud.objects.get(pk=self.request.GET.get('solicitud_id', None))
        return context
