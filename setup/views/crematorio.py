from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from apps.localizations.models.department import Department
from apps.util.generic_filters.views import FilteredListView
from apps.util.valid_user_access_views import valid_access_view, valid_group_access
from setup.forms.crematorio import CrematorioListFilter, CrematorioForm
from setup.models.crematorio import Crematorio

departments = Department.objects.all()


class CrematorioList(FilteredListView):
    model = Crematorio
    paginate_by = 30
    form_class = CrematorioListFilter
    filter_fields = []
    search_fields = ['nombre', ]
    default_order = '-id'

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CrematorioList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        title = "Todos los crematorios"
        return dict(
            super(CrematorioList, self).get_context_data(**kwargs), title=title)


class CrematorioCreate(CreateView):
    model = Crematorio
    form_class = CrematorioForm
    success_url = reverse_lazy('crematorio:list')

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CrematorioCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        msg = "Crematorio agregado correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        title = "Nuevo Crematorio"
        return dict(
            super(CrematorioCreate, self).get_context_data(**kwargs), title=title, departments=departments)


class CrematorioUpdate(UpdateView):
    model = Crematorio
    form_class = CrematorioForm
    success_url = reverse_lazy('crematorio:list')

    # @method_decorator(valid_access_view(valid_entidad, login_url='/validate'))
    # def dispatch(self, *args, **kwargs):
    #     return super(CrematorioUpdate, self).dispatch(*args, **kwargs)

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CrematorioUpdate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        msg = "Crematorio editado correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        title = "Actualizar Crematorio"
        object = Crematorio.objects.get(pk=self.kwargs['pk'])
        return dict(
            super(CrematorioUpdate, self).get_context_data(**kwargs), title=title, departments=departments,
            departamento=object.distrito.province.department, provincia=object.distrito.province,
            distrito=object.distrito)
