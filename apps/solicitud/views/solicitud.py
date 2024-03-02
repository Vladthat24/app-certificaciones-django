from datetime import datetime

from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from apps.generic.models.anio import Anio
from apps.generic.models.rango_horario import RangoHorario
from apps.localizations.models.department import Department
from apps.solicitud.forms.solicitud import SolicitudListFilter, SolicitudForm, SolicitudListFilterDSAIA
from apps.solicitud.models.estado_observado import EstadoObservado
from apps.solicitud.models.solicitud import Solicitud
from apps.solicitud.util import get_fecha_registrado_valid, get_fecha_excluyendo_no_laborables_two
from apps.util.generic_filters.views import FilteredListView
from apps.util.get_group_user import get_group_user
from apps.util.valid_user_access_views import valid_access_view, valid_numero_expediente
from setup.models.menu import Menu

from django.utils.decorators import method_decorator

list_inputs_datos_personales = ['solicitante_numero_documento', 'solicitante_tipo_documento',
                                'solicitante_nombres', 'solicitante_apellido_paterno',
                                'solicitante_apellido_materno', 'solicitante_direccion',
                                'solicitante_departamento_name', 'solicitante_provincia_name',
                                'solicitante_distrito_name',
                                'solicitante_correo', 'solicitante_celular',
                                'solicitante_estado_civil', 'solicitante_parentesco']

list_inputs_datos_fallecido = ['fallecido_tipo_documento', 'fallecido_numero_documento', 'fallecido_nombres',
                               'fallecido_apellido_paterno', 'fallecido_apellido_materno', 'fallecido_sexo',
                               'fallecido_fecha_nacimiento',
                               'fallecido_estado_civil', 'fallecido_fecha_fallecimiento', 'fallecido_parentesco']

list_inputs_datos_fallecido_others = ['numero_necropsia', 'fecha_necropsia']

list_inputs_lugar_fallecimiento = ['lugar_fallecimiento_tipo', 'lugar_fallecimiento_preposicion_titulo']

list_inputs_lugar_fallecimiento_others = ['lugar_fallecimiento_direccion', ]

departments = Department.objects.all()

list_hiden = ["created_ip", "created_by"]


class SolicitudList(FilteredListView):
    model = Solicitud
    paginate_by = 20
    form_class = SolicitudListFilter
    filter_fields = ['es_covid', 'estado', 'solicitante_tipo_documento', 'fallecido_tipo_documento']
    search_fields = ['solicitante_numero_documento', 'solicitante_nombres', 'solicitante_apellido_paterno',
                     'fallecido_numero_documento', 'fallecido_nombres', 'fallecido_apellido_paterno',
                     'fallecido_apellido_materno', 'numero_expediente']
    default_order = 'estado'

    def get_form_class(self):
        """Return the form class to use."""

        group = get_group_user(self.request)

        if group == 4:
            return SolicitudListFilterDSAIA

        return SolicitudListFilter

    def get_filters(self):

        group = get_group_user(self.request)

        if group == 4:
            filters = super().get_filters_customized(
                ['es_covid', 'estado', 'solicitante_tipo_documento', 'fallecido_tipo_documento'])
        else:
            filters = super().get_filters_customized(
                ['es_covid', 'solicitante_tipo_documento', 'fallecido_tipo_documento'])

        return filters

    @property
    def form(self):
        group = get_group_user(self.request)

        if group == 4:
            filter_ = ['es_covid', 'estado', 'solicitante_tipo_documento', 'fallecido_tipo_documento']
        else:
            filter_ = ['es_covid', 'solicitante_tipo_documento', 'fallecido_tipo_documento']

        try:
            return self._form
        except AttributeError:
            form_class = self.get_form_class()
        self._form = self.get_form(form_class)

        # Hide filter_fields
        if hasattr(self, 'filter_fields'):
            for fieldname in filter_:
                field = self._form.fields[fieldname]
                hidden_widget = getattr(field, 'hidden_widget',
                                        forms.HiddenInput)
                field.widget = hidden_widget()

        return self._form

    def get_context_data(self, **kwargs):
        title = "Lista de solicitudes."
        group = get_group_user(self.request)
        tipo = "normal"

        if self.request.get_full_path().find("observadas") > 0:
            tipo = "observado"

        return dict(
            super(SolicitudList, self).get_context_data(**kwargs), title=title, tipo=tipo, group=group)

    def get_queryset(self):
        queryset = super().get_queryset()

        group = get_group_user(self.request)

        if group == 1:
            entidad_id = self.request.session['entidad_id']
            if self.request.get_full_path().find("observadas") > 0:
                queryset = queryset.filter(crematorio_id=int(entidad_id), estado_observado__in=[1, 2]).order_by(
                    'estado').distinct()
            else:
                queryset = queryset.filter(crematorio_id=int(entidad_id), estado_observado=0).order_by('estado',
                                                                                                       '-fecha_envio')
        if group == 2:
            if self.request.get_full_path().find("validadas") > 0:
                queryset = queryset.filter(tesoreria_valid=True).order_by('estado', '-created_at').distinct()

            elif self.request.get_full_path().find("observadas") > 0:

                queryset = queryset.distinct().filter(estado=1, tesoreria_valid=False,
                                                      estados__created_by=self.request.user).order_by('estado',
                                                                                                      '-created_at')
            else:
                queryset = queryset.distinct().filter(estado=1, tesoreria_valid=False).order_by('estado',
                                                                                                '-created_at').exclude(
                    estados__created_by=self.request.user)

        if group == 3:
            if self.request.get_full_path().find("observadas") > 0:
                queryset = queryset.filter(tesoreria_valid=True, estados__created_by=self.request.user).distinct(). \
                    order_by('estado', '-registrado_fecha')

            else:
                queryset = queryset.filter(tesoreria_valid=True).order_by('estado', '-fecha_envio').exclude(
                    estados__created_by=self.request.user).distinct()

        if group == 4:
            estados = [2, 4, 5]
            if self.request.get_full_path().find("observadas") > 0:
                queryset = queryset.distinct().filter(estado__in=estados,
                                                      estados__created_by=self.request.user).distinct(). \
                    order_by('-created_at')
            else:
                queryset = queryset.distinct().filter(estado__in=estados).order_by('-created_at'). \
                    exclude(estados__created_by=self.request.user)

        try:
            # self.request.session["anio_current"]
            try:
                anio = Anio.objects.get(pk=self.request.session["anio_current"]["id"])
                queryset = queryset.filter(created_at__year=anio.nombre)

            except Anio.DoesNotExist:
                print(" Anio no existe ")

        except KeyError:
            queryset = queryset.filter(created_at__year=datetime.now().year)

        return queryset

    # self.request.session["anio_current"]


class SolicitudCreate(CreateView):
    model = Solicitud
    form_class = SolicitudForm

    def get_context_data(self, **kwargs):
        # TODO, Validar a que entidad pertenece el usuario logeado (Crematorio, Cementerio, etc)
        title = "SOLICITUD DE AUTORIZACIÓN SANITARIA PARA LA CREMACIÓN DE CADAVER"

        return dict(
            super(SolicitudCreate, self).get_context_data(**kwargs), title=title, departments=departments,
            list_inputs_datos_personales=list_inputs_datos_personales,
            list_inputs_datos_fallecido=list_inputs_datos_fallecido,
            list_inputs_lugar_fallecimiento=list_inputs_lugar_fallecimiento,
            list_inputs_lugar_fallecimiento_others=list_inputs_lugar_fallecimiento_others,
            list_inputs_datos_fallecido_others=list_inputs_datos_fallecido_others, list_hiden=list_hiden)

    def form_valid(self, form):
        msg = "La solicitud fue agregada correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        self.object = form.save()

        hospital_id = int(self.request.POST.get('hospital_id', 0))
        crematorio_id = int(self.request.session['entidad_id'])

        if hospital_id > 0:
            self.object.lugar_fallecimiento_hospital_id = hospital_id
            self.object.save()

        if crematorio_id:
            self.object.crematorio_id = crematorio_id
            self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        # return reverse_lazy('department:province-list', kwargs={'department_id': self.kwargs['department_id']})
        return reverse_lazy('solicitud:list', kwargs={})


class SolicitudUpdate(UpdateView):
    model = Solicitud
    form_class = SolicitudForm


    @method_decorator(valid_access_view(valid_numero_expediente, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(SolicitudUpdate, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        title = "SOLICITUD DE AUTORIZACIÓN SANITARIA PARA LA CREMACIÓN DE CADAVER"
        object = Solicitud.objects.get(pk=self.kwargs['pk'])

        hospital = object.lugar_fallecimiento_hospital

        referer = ""
        if self.request.META.get('HTTP_REFERER'):
            if len(self.request.META.get('HTTP_REFERER').split("?")) > 1:
                referer = "?" + self.request.META.get('HTTP_REFERER').split("?")[-1]

        return_dict = dict(
            super(SolicitudUpdate, self).get_context_data(**kwargs), title=title, departments=departments,
            list_inputs_datos_personales=list_inputs_datos_personales,
            list_inputs_datos_fallecido=list_inputs_datos_fallecido,
            list_inputs_lugar_fallecimiento=list_inputs_lugar_fallecimiento,
            list_inputs_lugar_fallecimiento_others=list_inputs_lugar_fallecimiento_others,
            hospital=hospital,
            list_inputs_datos_fallecido_others=list_inputs_datos_fallecido_others,
            list_hiden=list_hiden
        )

        return_dict["referer"] = referer

        if object.lugar_fallecimiento_distrito:
            return_dict['fallecido_departamento'] = object.lugar_fallecimiento_distrito.province.department
            return_dict['fallecido_provincia'] = object.lugar_fallecimiento_distrito.province
            return_dict['fallecido_distrito'] = object.lugar_fallecimiento_distrito
        #
        # fallecido_departamento = object.lugar_fallecimiento_distrito.province.department,
        # fallecido_provincia = object.lugar_fallecimiento_distrito.province,
        # fallecido_distrito = object.lugar_fallecimiento_distrito,

        return return_dict

    def form_valid(self, form):
        msg = "La solicitud fue editada correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)

        instance_temp = Solicitud.objects.get(pk=form.instance.id)

        if instance_temp.numero_expediente:
            self.object.archivo = instance_temp.archivo
            self.object.constancia_deposito = instance_temp.constancia_deposito
        self.object = form.save()

        hospital_id = 0 if self.request.POST.get('hospital_id', 0) == "" else int(
            self.request.POST.get('hospital_id', 0))
        crematorio_id = int(self.request.session['entidad_id'])

        if hospital_id > 0:
            self.object.lugar_fallecimiento_hospital_id = hospital_id
            self.object.save()

        if crematorio_id:
            self.object.crematorio_id = crematorio_id
            self.object.save()

        if self.object.estado == 3:
            self.object.estado = 1
            self.object.save()
            #     if self.estado == 3:
            #         self.estado = 1

        return super().form_valid(form)

    def get_success_url(self):

        referer = self.request.POST.get("referer", "")
        # if self.request.META.get('HTTP_REFERER'):
        #     if len(self.request.META.get('HTTP_REFERER').split("?")) > 1:
        #         referer = "?" + self.request.META.get('HTTP_REFERER').split("?")[-1]

        if "Observadas" in self.request.session['menu_children_name']:
            return reverse_lazy('solicitud:list-observadas', kwargs={}) + referer

        return reverse_lazy('solicitud:list', kwargs={}) + referer


class SolicitudDelete(DeleteView):
    success_url = reverse_lazy('solicitud:list')
    model = Solicitud

    @method_decorator(valid_access_view(valid_numero_expediente, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(SolicitudDelete, self).dispatch(*args, **kwargs)


class SolicitudDetailView(DetailView):
    model = Solicitud
    template_name = "solicitud/solicitud_detail.html"



    def get_context_data(self, **kwargs):
        title = "SOLICITUD DE AUTORIZACIÓN SANITARIA PARA LA CREMACIÓN DE CADAVER"

        # referer = "/" + '/'.join(self.request.META.get('HTTP_REFERER').split("/")[3:])

        referer = ""
        if self.request.META.get('HTTP_REFERER'):
            if len(self.request.META.get('HTTP_REFERER').split("?")) > 1:
                referer = "?" + self.request.META.get('HTTP_REFERER').split("?")[-1]

        group = get_group_user(self.request)
        menu = Menu.objects.get(pk=self.request.session['menu_children'])

        tipo_menu_acceso = 0
        if menu.name.find("Observadas") > 0:
            tipo_menu_acceso = 1
        if menu.name.find("Validadas") > 0:
            tipo_menu_acceso = 2

        return dict(
            super(SolicitudDetailView, self).get_context_data(**kwargs), title=title, referer=referer, group=group,
            tipo_menu_acceso=tipo_menu_acceso)


def save_nro_expediente(request):
    if request.POST:
        solicitud_id = request.POST.get('solicitud_id', None)
        nro_expediente = request.POST.get('nro_expediente', None)

        if not solicitud_id or not nro_expediente:
            msg = "Error al Guardar el número de expediente."
            messages.add_message(request, messages.SUCCESS, msg, extra_tags="danger")
            return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))

        solicitud = Solicitud.objects.get(pk=int(solicitud_id))

        solicitud.numero_expediente = nro_expediente
        solicitud.estado = 2

        try:
            RangoHorario.objects.get(state=True)
            solicitud.registrado_fecha = get_fecha_excluyendo_no_laborables_two(datetime.now())
        except RangoHorario.DoesNotExist:
            solicitud.registrado_fecha = get_fecha_registrado_valid(datetime.now())

        # solicitud.registrado_fecha = get_fecha_excluyendo_no_laborables()
        # solicitud.registrado_fecha = get_fecha_excluyendo_no_laborables_two(datetime.now())
        # solicitud.registrado_fecha = datetime.now()
        solicitud.save()

    msg = "Número de expediente guardado correctamente."
    messages.add_message(request, messages.SUCCESS, msg, extra_tags="success")

    return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))


def aprobar_solicitud_tesoreria(request):
    if request.POST:
        solicitud_id = request.POST['solicitud_id']
        solicitud = Solicitud.objects.get(pk=int(solicitud_id))
        solicitud.tesoreria_valid = True
        solicitud.validacion_tesoreria_fecha = datetime.now()

        solicitud.save()

        msg = "Solicitud aprobada correctamente"
        messages.add_message(request, messages.SUCCESS, msg, extra_tags="success")
        return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))


def guardar_escaneado(request):
    if request.POST:
        solicitud_id = request.POST['solicitud_id']
        solicitud = Solicitud.objects.get(pk=int(solicitud_id))
        try:
            escaneado = request.FILES['escaneado']
            solicitud.escaneado = escaneado
            solicitud.estado = 5
            solicitud.save()
        except MultiValueDictKeyError:
            print("Error")

        msg = "Archivo agragando correctamente."
        messages.add_message(request, messages.SUCCESS, msg, extra_tags="success")
        return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))

    else:
        solicitud_id = request.GET.get('solicitud_id', 0)
        solicitud = Solicitud.objects.get(pk=solicitud_id)
        template = loader.get_template('solicitud/form_escaneado.html')
        return HttpResponse(template.render({'solicitud': solicitud}, request))


def eliminar_escaneado(request):
    if request.POST:
        solicitud_id = request.POST['solicitud_id']
        try:
            solicitud = Solicitud.objects.get(pk=int(solicitud_id))
            solicitud.escaneado = None
            solicitud.estado = 4
            solicitud.save()
        except Solicitud.DoesNotExist:
            print("Solicitud no existe.")

        msg = "Archivo eliminado correctamente."
        messages.add_message(request, messages.SUCCESS, msg, extra_tags="info")
        return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))

    else:
        msg = "Error al eliminar archivo."
        messages.add_message(request, messages.SUCCESS, msg, extra_tags="danger")
        return HttpResponse('Error')


def levantar_observacion_solicitud(request):
    solicitud_id = request.POST.get('solicitud_id', None)
    descargo = request.POST.get('descargo', None)
    archivo = None
    try:
        archivo = request.FILES['archivo']
    except MultiValueDictKeyError as e:
        print(e)

    if not solicitud_id:
        msg = "Error al  levantar la observación."
        messages.add_message(request, messages.SUCCESS, msg, extra_tags="danger")
        return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))

    try:
        solicitud = Solicitud.objects.get(pk=int(solicitud_id))

        group = get_group_user(request)

        estado_observado = solicitud.get_estado_observado_oficina()["estado_observado"]

        if group == 1 and estado_observado == 1:
            msg = "Error al  levantar la observación."
            messages.add_message(request, messages.SUCCESS, msg, extra_tags="danger")
            return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))

        # solicitud.estado = 1
        solicitud.estado_observado = 2
        solicitud.save()
        estado = EstadoObservado.objects.filter(solicitud=solicitud).last()
        estado.descargo = descargo
        estado.descargo_archivo = archivo
        estado.estado = 2
        estado.save()
    except Solicitud.DoesNotExist:
        print(" Solicitud No existe")

    return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))


def observar_solicitud(request):
    solicitud_id = request.POST.get('solicitud_id', None)
    observaciones = request.POST.get('observaciones', None)

    if not solicitud_id:
        msg = "Error al observar la solicitud."
        messages.add_message(request, messages.SUCCESS, msg, extra_tags="danger")
        return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))

    archivo = None
    try:
        archivo = request.FILES['archivo']
    except MultiValueDictKeyError as e:
        print(e)

    try:
        solicitud = Solicitud.objects.get(pk=int(solicitud_id))

        group = get_group_user(request)

        estado_observado = solicitud.get_estado_observado_oficina()["estado_observado"]

        estado_final = False

        if group == 1 and estado_observado == 1:
            estado_final = True

        if group > 1 and (estado_observado == 0 or estado_observado == 2):
            estado_final = True

        if not estado_final:
            msg = "Error al observar la solicitud."
            messages.add_message(request, messages.SUCCESS, msg, extra_tags="danger")
            return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))

        # solicitud.estado = 3
        solicitud.estado_observado = 1
        solicitud.save()
        estado = EstadoObservado(solicitud=solicitud, observacion=observaciones, observacion_archivo=archivo)
        estado.save()
    except Solicitud.DoesNotExist:
        print(" Solicitud No existe")

    msg = "Solicitud observada correctamente."
    messages.add_message(request, messages.SUCCESS, msg, extra_tags="info")
    return redirect("/" + '/'.join(request.META.get('HTTP_REFERER').split("/")[3:]))
