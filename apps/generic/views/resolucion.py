from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.generic.forms.resolucion import ResolucionListFilter, ResolucionForm
from apps.generic.models.resolucion import Resolucion
from apps.util.generic_filters.views import FilteredListView


class ResolucionList(FilteredListView):
    model = Resolucion
    paginate_by = 10
    form_class = ResolucionListFilter
    filter_fields = []
    search_fields = ['nombre_director']
    default_order = '-id'

    def get_context_data(self, **kwargs):
        title = "Todas las resoluciones"
        return dict(
            super(ResolucionList, self).get_context_data(**kwargs), title=title)


class ResolucionCreate(CreateView):
    model = Resolucion
    form_class = ResolucionForm
    success_url = reverse_lazy('resolucion:list')

    def form_valid(self, form):
        msg = "Resolución creada correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)


class ResolucionUpdate(UpdateView):
    model = Resolucion
    form_class = ResolucionForm
    success_url = reverse_lazy('resolucion:list')

    def form_valid(self, form):
        msg = "Resolución actualizada correctamente"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)
