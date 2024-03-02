from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.localizations.forms.department import DepartmentForm, DepartmentListFilter
from apps.localizations.models.country import Country
from apps.localizations.models.department import Department
from apps.util.generic_filters.views import FilteredListView
from apps.util.views.dropdown_list import dropdown_list


class DepartmentList(FilteredListView):
    model = Department
    paginate_by = 10
    form_class = DepartmentListFilter
    filter_fields = []
    search_fields = ['name']
    default_order = '-id'

    def get_context_data(self, **kwargs):
        country = Country.objects.get(pk=self.kwargs['country_id'])
        title = "Lista de Departamentos del " + country.name + "."

        return dict(
            super(DepartmentList, self).get_context_data(**kwargs), title=title, country=country)

    def get_queryset(self):
        return Department.objects.filter(country_id=self.kwargs['country_id'])


class DepartmentCreate(CreateView):
    model = Department
    form_class = DepartmentForm

    def get_context_data(self, **kwargs):
        country = Country.objects.get(pk=self.kwargs['country_id'])
        title = "Agregar departamento"

        return dict(
            super(DepartmentCreate, self).get_context_data(**kwargs), title=title, country=country)

    def get_success_url(self):
        return reverse_lazy('country:department-list', kwargs={'country_id': self.kwargs['country_id']})


class DepartmentUpdate(UpdateView):
    model = Department
    form_class = DepartmentForm

    def get_context_data(self, **kwargs):
        country = Country.objects.get(pk=self.kwargs['country_id'])
        title = "Editar departamento"

        return dict(
            super(DepartmentUpdate, self).get_context_data(**kwargs), title=title, country=country)

    def get_success_url(self):
        return reverse_lazy('country:department-list', kwargs={'country_id': self.kwargs['country_id']})


def dropdown_department(request):
    department_list = []
    if request.GET.get('country_id'):
        department_list = Department.objects.filter(country_id=request.GET.get('country_id'))
    return dropdown_list(request=request, list=department_list)
