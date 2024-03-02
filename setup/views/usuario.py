import os
import sys

from setup.models.entidad import Entidad

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass

# django.setup()

from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView

from apps.util.generic_filters.views import FilteredListView
from apps.util.valid_user_access_views import valid_access_view, permission_and_entidad, valid_group_access
from setup.forms.usuario import UsuarioListFilter, UsuarioForm, UsuarioChangeForm, UsuarioChangePasswordForm
from setup.models.usuario import Usuario


class UsuarioList(FilteredListView):
    model = Usuario
    paginate_by = 30
    form_class = UsuarioListFilter
    search_fields = ['username', 'first_name', 'last_name', 'document']
    default_order = 'id'

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioList, self).dispatch(*args, **kwargs)

    # @method_decorator(valid_access_view(permission_and_entidad, login_url='/validate'))
    # def dispatch(self, *args, **kwargs):
    #     return super(UsuarioList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        title = "Todos los usuarios"
        return dict(
            super(UsuarioList, self).get_context_data(**kwargs), title=title)

    def get_queryset(self):
        groups = [g.id for g in Group.objects.filter(name__in=['Administrador', 'Trabajador'])]

        queryset = super().get_queryset()
        # return queryset.filter(is_staff=False).exclude(groups__in=groups).order_by('-id')
        return queryset.filter(is_staff=False).order_by('-id')


class UsuarioCreate(CreateView):
    form_class = UsuarioForm
    model = Usuario
    success_url = reverse_lazy('usuario:list')

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        groups = self.request.POST.getlist("groups")
        project = self.request.POST.getlist("project")

        persona = Usuario.objects.get(pk=self.object.id)

        if groups:
            grupos = Group.objects.filter(id__in=groups)
            for g in grupos:
                persona.groups.add(g)
                persona.save()

        msg = "El Usuario <strong>" + str(self.request.POST['username']) + "</strong>  fue agregado correctamente"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        title = "Agregar Usuario"
        return dict(
            super(UsuarioCreate, self).get_context_data(**kwargs), title=title)


class UsuarioUpdate(UpdateView):
    form_class = UsuarioChangeForm
    model = Usuario
    success_url = reverse_lazy('usuario:list')

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(UsuarioUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        usuario = Usuario.objects.get(pk=self.kwargs['pk'])
        title = "Actualizar Usuario"
        groups = [g.name for g in usuario.groups.all()]
        return dict(
            super(UsuarioUpdate, self).get_context_data(**kwargs), usuario=usuario, title=title, groups=groups)

    def form_valid(self, form):
        msg = "El Usuario <strong>" + str(
            self.request.POST['username'] + "</strong>  fue editado correctamente")
        messages.add_message(self.request, messages.SUCCESS, msg)
        self.object = form.save(commit=False)
        grupos = self.request.POST.getlist('groups')
        groups_name = [g.name for g in Group.objects.filter(id__in=grupos)]

        self.object.entidad = None
        self.object.ris = 0

        for g in groups_name:
            if g == "Administrador RIS":
                self.object.ris = self.request.POST['ris']
            if g == "Administrador IPRESS":
                if self.request.POST['entidad']:
                    self.object.entidad = Entidad.objects.get(pk=self.request.POST['entidad'])
        self.object.save()

        return super().form_valid(form)


class UserPasswordUpdate(UpdateView):
    form_class = UsuarioChangePasswordForm
    model = Usuario
    template_name = "setup/change_password.html"

    def get_success_url(self):
        return reverse_lazy('usuario:edit',
                            kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        user_object = Usuario.objects.get(pk=self.kwargs['pk'])
        title = "Actualizar contraseña"

        return dict(
            super(UserPasswordUpdate, self).get_context_data(**kwargs), user_object=user_object, title=title)

    def form_valid(self, form):
        msg = "Contraseña actualizada del usuario: <strong>" + str(
            self.request.POST['username'] + "</strong>")
        messages.add_message(self.request, messages.SUCCESS, msg)

        return super().form_valid(form)
#
#
# def PersonSerializer(person):
#     return {'id': person.id, 'first_name': person.first_name, 'last_name': person.last_name}
#
#
# def PersonSearch(request):
#     q = request.GET.get('q')
#     print(q)
#
#     list_person = Person.objects.filter(
#         Q(first_name__startswith=q) | Q(last_name__startswith=q)
#         | Q(first_name__icontains=q) | Q(last_name__icontains=q)
#         | Q(document__startswith=q) | Q(document__icontains=q))
#     list_person_ = [PersonSerializer(p) for p in list_person]
#
#     return HttpResponse(json.dumps(list_person_), content_type='application/json')
#
#
# def PersonSerializerBasic(person):
#     return {'id': person.id, 'name': person.first_name + " " + person.last_name}
#
#
# def person_all_json(request):
#     list_person = Person.objects.all()
#     list_person_ = [PersonSerializerBasic(p) for p in list_person]
#     return HttpResponse(json.dumps(list_person_), content_type='application/json')
#
#
# class PersonDelete(DeleteView):
#     model = Person
#     success_url = reverse_lazy('person:list')
