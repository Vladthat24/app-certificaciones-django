from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.localizations.forms.province import ProvinceForm, ProvinceListFilter
from apps.localizations.models.department import Department
from apps.localizations.models.province import Province
from apps.util.generic_filters.views import FilteredListView
from apps.util.views.dropdown_list import dropdown_list


class ProvinceList(FilteredListView):
    model = Province
    paginate_by = 10
    form_class = ProvinceListFilter
    filter_fields = []
    search_fields = ['name']
    default_order = '-id'

    def get_context_data(self, **kwargs):
        department = Department.objects.get(pk=self.kwargs['department_id'])
        title = "Lista de Provincias del Departamento de " + department.name + "."

        return dict(
            super(ProvinceList, self).get_context_data(**kwargs), title=title, country=department.country,
            department=department)

    def get_queryset(self):
        return Province.objects.filter(department_id=self.kwargs['department_id'])


class ProvinceCreate(CreateView):
    model = Province
    form_class = ProvinceForm

    def get_context_data(self, **kwargs):
        department = Department.objects.get(pk=self.kwargs['department_id'])
        title = "Nueva provincia"

        return dict(
            super(ProvinceCreate, self).get_context_data(**kwargs), title=title, country=department.country,
            department=department)

    def get_success_url(self):
        return reverse_lazy('department:province-list', kwargs={'department_id': self.kwargs['department_id']})


class ProvinceUpdate(UpdateView):
    model = Province
    form_class = ProvinceForm

    def get_context_data(self, **kwargs):
        department = Department.objects.get(pk=self.kwargs['department_id'])
        title = "Editar provincia"

        return dict(
            super(ProvinceUpdate, self).get_context_data(**kwargs), title=title, country=department.country,
            department=department)

    def get_success_url(self):
        return reverse_lazy('department:province-list', kwargs={'department_id': self.kwargs['department_id']})


def dropdown_province(request):
    province_list = []
    if request.GET.get('department_id'):
        province_list = Province.objects.filter(department_id=request.GET.get('department_id'))
    return dropdown_list(request=request, list=province_list)
