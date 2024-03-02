import json

from django.contrib import messages
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.localizations.models.department import Department
from apps.solicitud.forms.hospital import HospitalListFilter, HospitalForm
from apps.solicitud.models.hospital import Hospital
from apps.util.generic_filters.views import FilteredListView

list_hiden = [
    'institucion', 'codigo_unico', 'clasificacion', 'tipo',
    'codigo_disa', 'codigo_red', 'codigo_microred', 'disa', 'red', 'microred', 'categoria', 'telefono', 'director',
    'estado', 'norte', 'este', 'ruc']


def HospitalSerializerBasic(object):
    return {'id': object.id, 'value': object.nombre_establecimiento.upper(), 'direccion': object.direccion,
            'distrito': object.distrito.name,
            'provincia': object.distrito.province.name, 'departamento': object.distrito.province.department.name}


def hospital_all_json(request):
    list_hospital = Hospital.objects.all()
    list_hospital_ = [HospitalSerializerBasic(p) for p in list_hospital]
    return HttpResponse(json.dumps(list_hospital_), content_type='application/json')


def hospital_filter_json(request):
    term = request.GET.get('term', '0')
    list_hospital = Hospital.objects.filter(nombre_establecimiento__icontains=term)[:15]
    list_hospital_ = [HospitalSerializerBasic(p) for p in list_hospital]
    return HttpResponse(json.dumps(list_hospital_), content_type='application/json')


class HospitalList(FilteredListView):
    model = Hospital
    paginate_by = 30
    form_class = HospitalListFilter
    filter_fields = []
    search_fields = ['nombre_establecimiento']
    default_order = '-id'

    def get_context_data(self, **kwargs):
        title = "Todas los hospitales"
        return dict(
            super(HospitalList, self).get_context_data(**kwargs), title=title)


class HospitalCreate(CreateView):
    model = Hospital
    form_class = HospitalForm
    success_url = reverse_lazy('hospital:list')

    def get_success_url(self):
        referer = self.request.POST.get('referer', None)
        if referer:
            return reverse_lazy('hospital:list') + referer
        return reverse_lazy('hospital:list')

    def get_context_data(self, **kwargs):
        departments = Department.objects.all()
        title = "Crear hospital."
        referer = ""
        if len(self.request.META.get('HTTP_REFERER').split("?")) > 1:
            referer = "?" + self.request.META.get('HTTP_REFERER').split("?")[-1]
        return dict(
            super(HospitalCreate, self).get_context_data(**kwargs), title=title, referer=referer,
            departments=departments, list_hiden=list_hiden)

    def form_valid(self, form):
        msg = "Hospital actualizado correctamente"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)


class HospitalUpdate(UpdateView):
    model = Hospital
    form_class = HospitalForm

    # success_url = reverse_lazy('hospital:list')

    def get_success_url(self):

        referer = self.request.POST.get('referer', None)
        if referer:
            return reverse_lazy('hospital:list') + referer
        return reverse_lazy('hospital:list')

    def get_context_data(self, **kwargs):
        departments = Department.objects.all()
        instance = Hospital.objects.get(pk=self.kwargs['pk'])
        title = "Actualizar hospital."
        referer = ""
        if self.request.META.get('HTTP_REFERER'):
            if len(self.request.META.get('HTTP_REFERER').split("?")) > 1:
                referer = "?" + self.request.META.get('HTTP_REFERER').split("?")[-1]
        return dict(
            super(HospitalUpdate, self).get_context_data(**kwargs), title=title, referer=referer,
            instance=instance, departments=departments, list_hiden=list_hiden)

    def form_valid(self, form):
        msg = "El hospital fue editado correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)
