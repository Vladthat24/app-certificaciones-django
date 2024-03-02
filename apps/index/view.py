from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from apps.generic.models.anio import Anio
from setup.models.crematorio import Crematorio
from setup.models.menu import Menu, GroupMenu
from setup.models.usuario import Usuario

ERROR_404_TEMPLATE_NAME = '404.html'
ERROR_403_TEMPLATE_NAME = '403.html'
ERROR_400_TEMPLATE_NAME = '400.html'
ERROR_500_TEMPLATE_NAME = '500.html'


class MenuItem(object):
    def __init__(self, id, name, url, icon):
        self.id = id
        self.name = name
        self.url = url
        self.icon = icon

    def serialize(self):
        return self.__dict__


def get_menu(user):
    group_list = list(col["id"] for col in Group.objects.values("id")
                      .filter(Q(user__id=user.id)).distinct())
    permission_list = list(col["id"] for col in Permission.objects
                           .values("id")
                           .filter(Q(group__in=group_list) | Q(user__id=user.id)).distinct())

    if user.is_superuser:
        menu_childrens_t = list(
            col["id"] for col in
            Menu.objects.values("id").all().order_by("id"))
    else:
        menu_childrens_t = list(
            col["menus"] for col in
            GroupMenu.objects.values("menus").filter(Q(group__in=group_list)).order_by("id"))

    menu_parents_parent = Menu.objects.filter(id__in=menu_childrens_t). \
        annotate(childrenss_num=Count('childrens')).filter(childrenss_num=0)

    menu_parents = Menu.objects.filter(childrens__in=menu_childrens_t).order_by("id").distinct()

    # list_menu = []
    menu_json = []
    menus_only_childrens = []

    for i in menu_parents:
        # childrens = []
        childrens_json = []

        for j in i.childrens.all():
            if j.id in menu_childrens_t:
                # childrens.append(j)
                childrens_json.append(MenuItem(j.id, j.name, j.url, j.icon).serialize())
                menus_only_childrens.append(j.id)
                menus_only_childrens.append(i.id)
        # list_menu.append({'menu': i, 'childrens': childrens})
        menu_json.append({'menu': MenuItem(i.id, i.name, i.url, i.icon).serialize(), 'childrens': childrens_json})

    menu_parents_final = menu_parents_parent.exclude(id__in=menus_only_childrens)

    for i in menu_parents_final:
        menu_json.append({'menu': MenuItem(i.id, i.name, i.url, i.icon).serialize(), 'childrens': []})

    return menu_json


class Validate(TemplateView):
    template_name = "validate.html"

    def get_context_data(self, **kwargs):
        # update_project_session(self.request)
        return dict(
            super(Validate, self).get_context_data(**kwargs))


def index(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({}, request))


class AnioItem(object):
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def serialize(self):
        return self.__dict__


class Dashboard(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        self.request.session["anio_list"] = [AnioItem(j.id, j.nombre).serialize() for j in Anio.objects.all()]

        msg = "Dashboard cargado. "
        messages.add_message(self.request, messages.SUCCESS, msg)

        try:
            self.request.session["anio_current"]
        except KeyError:
            self.request.session["anio_current"] = {"id": 1, "nombre": "2021"}

            if Anio.objects.filter(state=True).count() > 0:
                anio_current = Anio.objects.filter(state=True)[0]
                self.request.session["anio_current"] = AnioItem(anio_current.id, anio_current.nombre).serialize()

        return dict(
            super(Dashboard, self).get_context_data(**kwargs))


@never_cache
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_active = Usuario.objects.get(username=username)
            if not user_active.is_active:
                msg = "Cuenta suspendida, contacte con el administrador"
                messages.add_message(request, messages.WARNING, msg, extra_tags='danger')
                return redirect(reverse('index:index'))

        except Usuario.DoesNotExist:
            msg = "Datos de acceso incorrectos"
            messages.add_message(request, messages.WARNING, msg)
            return redirect(reverse('index:index'))

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)

                u = Usuario.objects.get(pk=user.id)

                request.session['user_full_name'] = u.username

                #
                if u.crematorio:
                    crematorio = Crematorio.objects.get(pk=u.crematorio.id)
                    request.session['entidad_nombre'] = crematorio.nombre.upper()
                    request.session['entidad_direccion'] = crematorio.direccion
                    request.session['entidad_id'] = crematorio.id
                else:
                    request.session['entidad_nombre'] = "DIRIS LM"
                    request.session['entidad_id'] = 0

                request.session["menu"] = get_menu(request.user)
                request.session["menu_manager"] = 'active'
                request.session["menu_patient"] = ''

                request.session['menu_parent'] = 2
                request.session["project"] = 0

                # return redirect(reverse('reclamo:entidad-reclamo-list'))
                # return render(request, 'dashboard.html')
                return redirect(reverse('index:dashboard'))
            else:
                msg = "Cuenta suspendida, contacte con el administrador"
                messages.add_message(request, messages.WARNING, msg)
                return redirect(reverse('index:index'))
        else:
            msg = "Datos de acceso incorrectos"
            messages.add_message(request, messages.WARNING, msg)
            return redirect(reverse('index:index'))
    else:
        msg = "Operación no soportada"
        messages.add_message(request, messages.WARNING, msg)
        return redirect(reverse('index:index'))


def logout_view(request):
    if request.user.is_authenticated:
        request.session['menu_children'] = 0
        request.session['menu_parent'] = 0
        logout(request)
    return redirect(reverse('index:index'))


list_tupa = "list_tupa.html"


class ListTupaView(TemplateView):
    template_name = list_tupa

    def get_context_data(self, *args, **kwargs):
        context = super(ListTupaView, self).get_context_data(**kwargs)
        return context


def change_anio(request):
    if request.user.is_authenticated:
        anio_id = request.GET.get('anio_id', '0')

        try:
            anio = Anio.objects.get(pk=int(anio_id))
            msg = "Cambiando al año: " + str(anio.nombre)
            messages.add_message(request, messages.INFO, msg)

            request.session["anio_current"] = AnioItem(anio.id, anio.nombre).serialize()

        except Anio.DoesNotExist:
            msg = "Ups, ocurrió un error"
            messages.add_message(request, messages.WARNING, msg, extra_tags="danger")

        return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))
        # return redirect(reverse('index:dashboard'))
