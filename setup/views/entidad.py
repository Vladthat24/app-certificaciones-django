from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from apps.util.generic_filters.views import FilteredListView
from apps.util.valid_user_access_views import is_manager_or_admin, valid_access_view, permission_and_entidad, \
    valid_entidad
from setup.forms.entidad import EntidadListFilter, EntidadForm
from setup.models.entidad import Entidad


class EntidadList(FilteredListView):
    model = Entidad
    paginate_by = 30
    form_class = EntidadListFilter
    filter_fields = []
    search_fields = ['nombre']
    default_order = '-id'

    @method_decorator(valid_access_view(permission_and_entidad, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(EntidadList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if len(self.request.user.groups.filter(name="Administrador UGIPRESS")) > 0:
            return queryset.order_by('-id')

        if len(self.request.user.groups.filter(name="Administrador IPRESS")) > 0:
            return queryset.filter(entidad_id=self.request.user.entidad.id).order_by('-id')

        if len(self.request.user.groups.filter(name="Administrador RIS")) > 0:
            return queryset.filter(ris=self.request.user.ris).order_by('-id')

        return queryset.filter(entidad_id=-5).order_by('-id')

    def get_context_data(self, **kwargs):
        title = "Todas las IPRESS"

        groups = self.request.user.groups.all()

        print(groups)

        return dict(
            super(EntidadList, self).get_context_data(**kwargs), title=title)


class EntidadCreate(CreateView):
    model = Entidad
    form_class = EntidadForm
    success_url = reverse_lazy('entidad:list')

    def form_valid(self, form):
        msg = "IPRESS agregada correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)

    # @method_decorator(user_passes_test(is_manager_or_admin, login_url='/reclamo/entidad-reclamo/list'))
    # def dispatch(self, *args, **kwargs):
    #     return super(EntidadCreate, self).dispatch(*args, **kwargs)


class EntidadUpdate(UpdateView):
    model = Entidad
    form_class = EntidadForm
    success_url = reverse_lazy('entidad:list')

    @method_decorator(valid_access_view(valid_entidad, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(EntidadUpdate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        msg = "IPRESS editada correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)
