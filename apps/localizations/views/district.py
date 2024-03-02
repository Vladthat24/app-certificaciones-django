import json

from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from apps.localizations.forms.district import DistrictForm, DistrictListFilter
from apps.localizations.models.district import District
from apps.localizations.models.province import Province
from apps.util.generic_filters.views import FilteredListView
from apps.util.views.dropdown_list import dropdown_list


class DistrictList(FilteredListView):
    model = District
    paginate_by = 10
    form_class = DistrictListFilter
    filter_fields = []
    search_fields = ['name']
    default_order = '-id'

    def get_context_data(self, **kwargs):
        province = Province.objects.get(pk=self.kwargs['province_id'])
        title = "Lista de Distritos de la Provincia de  " + province.name + "."

        return dict(
            super(DistrictList, self).get_context_data(**kwargs), title=title, country=province.department.country,
            department=province.department, province=province)

    def get_queryset(self):
        return District.objects.filter(province_id=self.kwargs['province_id'])


class DistrictCreate(CreateView):
    model = District
    form_class = DistrictForm

    def get_context_data(self, **kwargs):
        province = Province.objects.get(pk=self.kwargs['province_id'])
        title = "Nuevo Distrito de la Provincia de " + province.name + "."

        return dict(
            super(DistrictCreate, self).get_context_data(**kwargs), title=title, country=province.department.country,
            department=province.department, province=province)

    def get_success_url(self):
        return reverse_lazy('province:district-list', kwargs={'province_id': self.kwargs['province_id']})


class DistrictUpdate(UpdateView):
    model = District
    form_class = DistrictForm

    def get_context_data(self, **kwargs):
        province = Province.objects.get(pk=self.kwargs['province_id'])
        title = "Editar Distrito de la Provincia de " + province.name + "."

        return dict(
            super(DistrictUpdate, self).get_context_data(**kwargs), title=title, country=province.department.country,
            department=province.department, province=province)

    def get_success_url(self):
        return reverse_lazy('province:district-list', kwargs={'province_id': self.kwargs['province_id']})


def dropdown_district(request):
    district_list = []
    if request.GET.get('province_id'):
        district_list = District.objects.filter(province_id=request.GET.get('province_id'))
    return dropdown_list(request=request, list=district_list)


def district_serializer(object):
    return {'id': object.id, 'name': object.name, "province_id": object.province.id,
            "province_name": object.province.name, "department_id": object.province.department.id,
            "department_name": object.province.department.name,
            "country_id": object.province.department.country.id,
            "country_name": object.province.department.country.name}


def get_district_by_id(request, pk):
    return HttpResponse(json.dumps(district_serializer(District.objects.get(pk=pk))), content_type='application/json')


from django.db.models import Q


def district_serializer_autocomplete(object):
    return {'id': object.id,
            'value': "Departamento (" + object.province.department.name + ")   |   Provincia (" + object.province.name + ")   |   Distrito (" + object.name + ")"}


def get_district_autocomplete(request):
    query = request.GET.get('term', '0')

    district_list = District.objects.filter(Q(name__icontains=query)).order_by('name')[:8]
    list_json = [district_serializer_autocomplete(district) for district in district_list]

    return HttpResponse(json.dumps(list_json),
                        content_type='application/json')
