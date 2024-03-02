from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse

from apps.index.view import get_menu
from apps.solicitud.models.solicitud import Solicitud
from setup.models.entidad import Entidad


def valid_access_view(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request, request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def is_manager_or_admin(user):
    if user.is_superuser:
        return True
    else:
        return user.groups.filter(name='Administrador').exists()


def permission_and_entidad(request, user):
    path = request.get_full_path()
    menus = get_menu(user)
    menus_string = str(menus)

    if menus_string.find(path.split("?")[0]) > -1:
        valor_return = True
        if len(request.user.groups.all()) == 0:
            valor_return = False

        if len(request.user.groups.filter(name="Administrador IPRESS")) > 0:
            if request.user.entidad == None:
                valor_return = False

        if len(request.user.groups.filter(name="Administrador RIS")) > 0:
            if request.user.ris == 0:
                valor_return = False

        if len(request.user.groups.filter(name="Administrador UGIPRESS")) > 0:
            valor_return = True

    else:
        valor_return = False

    return valor_return


def valid_entidad(request, user):
    path = request.get_full_path()

    entidad_id = path.split("/")[-1]

    valor_return = False

    if len(request.user.groups.filter(name="Administrador RIS")) > 0:
        if request.user.ris > 0 and len(Entidad.objects.filter(ris=request.user.ris, pk=entidad_id)) > 0:
            valor_return = True

    if len(request.user.groups.filter(name="Administrador UGIPRESS")) > 0:
        valor_return = True

    return valor_return


def valid_ipress_entidad_add(request, user):
    valor_return = False

    if len(request.user.groups.filter(name="Administrador IPRESS")) > 0:
        if request.user.entidad:
            valor_return = True

    return valor_return


# Custom Decorator
def teacher_required(function):
    def _function(request, *args, **kwargs):
        # if request.user.groups.filter(name='Administrador').exists():
        return HttpResponseRedirect(reverse('lot.internal:list'))
        # return function(request, *args, **kwargs)

    return _function


def valid_group_access(request, user):
    if user.is_superuser:
        return True
    else:
        return user.groups.filter(name='ADMINISTRADOR DIRIS').exists()



def valid_numero_expediente(request, user):

    valor_return = False
    id = request.get_full_path().split("/")[-1:][0]
    instance_temp = Solicitud.objects.get(pk=id)

    if not instance_temp.numero_expediente:
        valor_return = True

    return valor_return
