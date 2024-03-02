from datetime import datetime

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView

from apps.certificacion.forms.certificacion import CertificacionsForm, CertificacionsListFilter, \
    CertificacionsModalForm, CertificacionsUpdateForm
from apps.certificacion.models.certificacion import Certificacion
from apps.generic.models.anio import Anio
from apps.solicitud.models.solicitud import Solicitud
from apps.util.generic_filters.views import FilteredListView
from apps.util.get_group_user import get_group_user
from apps.util.valid_user_access_views import valid_access_view, valid_group_access

list_disabled_in_modal = ['solicitante', 'dni', 'parentesco', 'fallecido_nombre', 'fallecido_fecha',
                          'necropsia_causa_muerte', 'necropsia_causa_muerte', 'necropsia_numero',
                          'fecha_cert_necropsia', 'created_ip', 'updated_ip', 'solicitud', 'tipo_otro', 'tipo', 'orden',
                          'solicitante_dni', 'fallecido_dni', 'fallecido_hora', 'parentesco_solicitante']


class CertificacionList(FilteredListView):
    model = Certificacion
    paginate_by = 15
    form_class = CertificacionsListFilter
    filter_fields = ['solicitud__es_covid', ]
    search_fields = ['numero_autorizacion', 'solicitud__numero_expediente', 'solicitud__fallecido_numero_documento',
                     'fallecido_nombre', ]
    default_order = '-created_at'

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CertificacionList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        title = "Lista de autorizaciones"
        return dict(
            super(CertificacionList, self).get_context_data(**kwargs), title=title, )

    def get_queryset(self):
        queryset = super().get_queryset()

        group = get_group_user(self.request)

        if group != 4:
            return queryset.filter(pk=0)

        try:
            a = self.request.session["anio_current"]
            try:
                anio = Anio.objects.get(pk=self.request.session["anio_current"]["id"])
                queryset = queryset.filter(created_at__year=anio.nombre)

            except Anio.DoesNotExist:
                print(" Anio no existe ")

        except KeyError:
            queryset = queryset.filter(created_at__year=datetime.now().year)

        return queryset


class CertificacionCreateModalView(CreateView):
    form_class = CertificacionsModalForm
    model = Certificacion
    template_name = 'certificacion/certificacion_form_modal.html'

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CertificacionCreateModalView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        msg = "Autorización agregada correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        self.object = form.save()
        self.object.solicitante = self.object.solicitud.get_solicitante()
        self.object.dni = self.object.solicitud.solicitante_numero_documento
        self.object.parentesco = self.object.solicitud.get_fallecido_parentesco_display()
        self.object.parentesco_solicitante = self.object.solicitud.get_solicitante_parentesco_display()
        self.object.fallecido_nombre = self.object.solicitud.get_fallecido()
        self.object.fallecido_fecha = self.object.solicitud.fallecido_fecha_fallecimiento
        self.object.solicitante_dni = self.object.solicitud.solicitante_numero_documento
        self.object.fallecido_dni = self.object.solicitud.fallecido_numero_documento
        self.object.fallecido_hora = self.object.solicitud.fallecido_hora_fallecimiento
        self.object.save()

        try:
            comprobante = self.request.FILES['comprobante']
            solicitud = Solicitud.objects.get(pk=self.object.solicitud_id)
            solicitud.comprobante = comprobante
            solicitud.save()
        except MultiValueDictKeyError:
            print(" Error ")
        return super().form_valid(form)

    def get_success_url(self):
        return "/" + '/'.join(self.request.META.get('HTTP_REFERER').split("/")[3:])

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CertificacionCreateModalView, self).get_form_kwargs(*args, **kwargs)
        solicitud = Solicitud.objects.filter(pk=int(self.kwargs['solicitud_pk'])).values_list('id',
                                                                                              'solicitante_numero_documento')[
                    0:1]
        kwargs['solicitud'] = solicitud
        return kwargs

    def get_initial(self):
        solicitud = int(self.kwargs['solicitud_pk'])
        autorizacion = Certificacion.objects.filter(numero_autorizacion__contains='-2024').first()
        if autorizacion:
            numero = autorizacion.numero_autorizacion.split("-")[0]
        else:
            numero = 0
        numero_autorizacion = str(int(numero) + 1).zfill(5) + "-2024"

        motivo = ""

        solicitud_object = Solicitud.objects.get(pk=solicitud)

        if solicitud_object.es_covid:
            motivo = 'Falleció por Covid 19, según consta en el Certificado de Defunción General obrante en el expediente.'
        return {
            'numero_autorizacion': numero_autorizacion,
            'solicitud': solicitud,
            'motivo': motivo,
            'fallecido_direccion': solicitud_object.get_direccion_fallecimiento()["direccion"],
        }

    def get_context_data(self, **kwargs):
        title = "Agregar certificación"
        solicitud = Solicitud.objects.get(pk=self.kwargs['solicitud_pk'])

        referer = ""

        if len(self.request.get_full_path().split("?")) > 1:
            referer = "?" + self.request.get_full_path().split("?")[-1]

        return dict(
            super(CertificacionCreateModalView, self).get_context_data(**kwargs), title=title, solicitud=solicitud,
            list_hidden=list_disabled_in_modal, referer=referer)


class CertificacionUpdateModalView(UpdateView):
    form_class = CertificacionsModalForm
    model = Certificacion
    template_name = 'certificacion/certificacion_form_modal.html'
    success_url = reverse_lazy('solicitud:list')

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CertificacionUpdateModalView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return "/" + '/'.join(self.request.META.get('HTTP_REFERER').split("/")[3:])

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CertificacionUpdateModalView, self).get_form_kwargs(*args, **kwargs)
        solicitud = Solicitud.objects.filter(pk=int(self.kwargs['solicitud_pk'])).values_list('id',
                                                                                              'solicitante_numero_documento')[
                    0:1]
        kwargs['solicitud'] = solicitud
        return kwargs

    def get_context_data(self, **kwargs):
        title = "Editar certificación"
        solicitud = Solicitud.objects.get(pk=self.kwargs['solicitud_pk'])

        referer = ""

        if len(self.request.get_full_path().split("?")) > 1:
            referer = "?" + self.request.get_full_path().split("?")[-1]

        return dict(
            super(CertificacionUpdateModalView, self).get_context_data(**kwargs), title=title, solicitud=solicitud,
            list_hidden=list_disabled_in_modal, referer=referer)

    def form_valid(self, form):
        msg = "Autorización actualizada correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        self.object = form.save()
        self.object.solicitante = self.object.solicitud.get_solicitante()
        self.object.dni = self.object.solicitud.solicitante_numero_documento
        self.object.parentesco = self.object.solicitud.solicitante_parentesco
        self.object.fallecido_nombre = self.object.solicitud.get_fallecido()
        self.object.fallecido_fecha = self.object.solicitud.fallecido_fecha_fallecimiento
        # self.object.fallecido_direccion = self.object.solicitud.get_direccion_fallecimiento()['direccion']
        self.object.save()

        try:
            comprobante = self.request.FILES['comprobante']
            solicitud = Solicitud.objects.get(pk=self.object.solicitud_id)
            solicitud.comprobante = comprobante
            solicitud.save()
        except MultiValueDictKeyError:
            print("Error")

        return super().form_valid(form)


class CertificacionCreateView(CreateView):
    form_class = CertificacionsForm
    model = Certificacion
    success_url = reverse_lazy('certificacion:list')

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CertificacionCreateView, self).dispatch(*args, **kwargs)

    # def get_success_url(self):
    #     return "/" + '/'.join(self.request.META.get('HTTP_REFERER').split("/")[3:])

    def get_initial(self):
        # autorizacion = Certificacion.objects.all().first()
        autorizacion = Certificacion.objects.filter(numero_autorizacion__contains='-2024').first()
        if autorizacion:
            numero = autorizacion.numero_autorizacion.split("-")[0]
        else:
            numero = 0

        numero_autorizacion = str(int(numero) + 1).zfill(5) + "-2024"

        return {
            'numero_autorizacion': numero_autorizacion,
            # 'solicitud': solicitud,
            'motivo': 'Falleció por',
        }

    def get_context_data(self, **kwargs):
        title = "Agregar autorización"
        # solicitud = Solicitud.objects.get(pk=)
        return dict(super(CertificacionCreateView, self).get_context_data(**kwargs), title=title,
                    list_hidden=list_disabled_in_modal)

    def form_valid(self, form):
        msg = "La autorización fue agregada correctamente"
        messages.add_message(self.request, messages.SUCCESS, msg)
        self.object = form.save()

        return super().form_valid(form)


class CertificacionUpdateView(UpdateView):
    form_class = CertificacionsUpdateForm
    model = Certificacion
    success_url = reverse_lazy('certificacion:list')

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CertificacionUpdateView, self).dispatch(*args, **kwargs)

    # def get_success_url(self):
    #     return "/" + '/'.join(self.request.META.get('HTTP_REFERER').split("/")[3:])

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CertificacionUpdateView, self).get_form_kwargs(*args, **kwargs)
        certificacion = Certificacion.objects.get(pk=self.kwargs['pk'])
        kwargs['tipo'] = certificacion.tipo
        kwargs['solicitud'] = certificacion.solicitud.id
        return kwargs

    def get_context_data(self, **kwargs):
        title = "Editar autorización"
        referer = ""
        if self.request.META.get('HTTP_REFERER'):
            if len(self.request.META.get('HTTP_REFERER').split("?")) > 1:
                referer = "?" + self.request.META.get('HTTP_REFERER').split("?")[-1]

        return dict(super(CertificacionUpdateView, self).get_context_data(**kwargs), title=title,
                    list_hidden=list_disabled_in_modal, referer=referer)

    def form_valid(self, form):
        msg = "La autorización fue actualizada correctamente"
        messages.add_message(self.request, messages.SUCCESS, msg)
        self.object = form.save()
        return super().form_valid(form)


class CertificacionDelete(DeleteView):
    success_url = reverse_lazy('certificacion:list')
    model = Certificacion

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(CertificacionDelete, self).dispatch(*args, **kwargs)

    # def get_success_url(self):
    #     return "/" + '/'.join(self.request.META.get('HTTP_REFERER').split("/")[3:])

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        certificacion = Certificacion.objects.get(pk=pk)
        if certificacion.solicitud:
            solicitud = Solicitud.objects.get(pk=certificacion.solicitud.id)
            solicitud.estado = 2
            solicitud.save()
        response = super(CertificacionDelete, self).delete(request, *args, **kwargs)

        return response


#

class Certificacion2UpdateModalView(UpdateView):
    # form_class = CertificacionsModal2Form
    # model = Certificacion
    # template_name = 'certificacion/solicitud_form_modal.html'
    form_class = CertificacionsModalForm
    model = Certificacion
    template_name = 'certificacion/certificacion_form_modal.html'

    @method_decorator(valid_access_view(valid_group_access, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(Certificacion2UpdateModalView, self).dispatch(*args, **kwargs)

    # success_url = reverse_lazy('certificacion:solicitud-list')

    def get_success_url(self):
        return "/" + '/'.join(self.request.META.get('HTTP_REFERER').split("/")[3:])

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(Certificacion2UpdateModalView, self).get_form_kwargs(*args, **kwargs)
        solicitud = Solicitud.objects.filter(pk=int(self.kwargs['solicitud_pk'])).values_list('id',
                                                                                              'solicitante_numero_documento')[
                    0:1]
        kwargs['solicitud'] = solicitud
        return kwargs

    def get_context_data(self, **kwargs):
        title = "Editar certificación"
        solicitud = Solicitud.objects.get(pk=self.kwargs['solicitud_pk'])

        return dict(
            super(Certificacion2UpdateModalView, self).get_context_data(**kwargs), title=title, solicitud=solicitud,
            list_hidden=list_disabled_in_modal)

    def form_valid(self, form):
        msg = "Autorización actualizada correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        self.object = form.save()
        self.object.solicitante = self.object.solicitud.get_solicitante()
        self.object.dni = self.object.solicitud.solicitante_numero_documento
        self.object.parentesco = self.object.solicitud.solicitante_parentesco
        self.object.fallecido_nombre = self.object.solicitud.get_fallecido()
        self.object.fallecido_fecha = self.object.solicitud.fallecido_fecha_fallecimiento
        # self.object.fallecido_direccion = self.object.solicitud.get_direccion_fallecimiento()['direccion']
        self.object.save()

        return super().form_valid(form)
