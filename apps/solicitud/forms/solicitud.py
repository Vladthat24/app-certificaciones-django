import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, Textarea
from django.utils.translation import gettext_lazy as _

from apps.solicitud.models.solicitud import Solicitud
from apps.util.generic_filters import forms as gf


class SolicitudForm(forms.ModelForm):
    hospital = forms.CharField(required=False)
    direccion_hospital = forms.CharField(required=False, widget=forms.Textarea())
    departamento_hospital = forms.CharField(required=False)
    provincia_hospital = forms.CharField(required=False)
    distrito_hospital = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['fallecido_parentesco'].choices = [('', '-- --')]

    def clean(self):
        cleaned_data = super().clean()
        state_error = False

        lugar_fallecimiento_tipo = cleaned_data.get("lugar_fallecimiento_tipo")
        hospital_id = cleaned_data.get("hospital_id")

        fallecido_fecha_nacimiento = cleaned_data.get("fallecido_fecha_nacimiento")
        fallecido_fecha_fallecimiento = cleaned_data.get("fallecido_fecha_fallecimiento")
        fecha_necropsia = cleaned_data.get("fecha_necropsia")
        fecha_deposito = cleaned_data.get("fecha_deposito")




        if fallecido_fecha_nacimiento and fallecido_fecha_fallecimiento and fecha_deposito:

            if fallecido_fecha_nacimiento > datetime.date.today():
                raise ValidationError("Error, La fecha de nacimiento no puede ser mayor al día de hoy")
            if fallecido_fecha_fallecimiento > datetime.date.today():
                raise ValidationError("Error, La fecha de fallecimiento no puede ser mayor al día de hoy")
            # if fecha_necropsia > datetime.date.today():
            #     raise ValidationError("Error, La fecha de necropcia no puede ser mayor al día de hoy")
            if fecha_deposito > datetime.date.today():
                raise ValidationError("Error, La fecha de deposito no puede ser mayor al día de hoy")

        else:
            if cleaned_data.get("fallecido_tipo_documento") != 4:
                raise ValidationError("Error, Ingrese una fecha ")

        solicitante_tipo_documento = cleaned_data.get("solicitante_tipo_documento")
        solicitante_numero_documento = cleaned_data.get("solicitante_numero_documento")
        solicitante_nombres = cleaned_data.get("solicitante_nombres")
        solicitante_apellido_paterno = cleaned_data.get("solicitante_apellido_paterno")
        solicitante_apellido_materno = cleaned_data.get("solicitante_apellido_materno")
        solicitante_estado_civil = cleaned_data.get("solicitante_estado_civil")

        if solicitante_tipo_documento != 5:
            if solicitante_numero_documento and solicitante_nombres and solicitante_apellido_paterno and solicitante_apellido_materno and solicitante_estado_civil:
                pass
            else:
                raise ValidationError("Error, Ingrese los datos del Solicitante")

        fallecido_tipo_documento = cleaned_data.get("fallecido_tipo_documento")
        fallecido_numero_documento = cleaned_data.get("fallecido_numero_documento")
        fallecido_nombres = cleaned_data.get("fallecido_nombres")
        fallecido_apellido_paterno = cleaned_data.get("fallecido_apellido_paterno")
        fallecido_apellido_materno = cleaned_data.get("fallecido_apellido_materno")

        fallecido_sexo = cleaned_data.get("fallecido_sexo")

        if fallecido_tipo_documento != 4:

            solicitudes_iguales = Solicitud.objects.filter(fallecido_tipo_documento=fallecido_tipo_documento,
                                                           fallecido_numero_documento=fallecido_numero_documento)

            if len(solicitudes_iguales) > 0:
                if solicitudes_iguales[0].id != self.instance.pk:
                    raise ValidationError("Error, Ya existe una solicitud con los datos del fallecido.")

            if fallecido_numero_documento and fallecido_nombres and fallecido_apellido_paterno and fallecido_apellido_materno and fallecido_sexo:
                pass
            else:
                raise ValidationError("Error, Ingrese los datos del Fallecido")

        solicitante_numero_documento = cleaned_data.get("solicitante_numero_documento")
        fallecido_numero_documento = cleaned_data.get("fallecido_numero_documento")

        if solicitante_numero_documento == fallecido_numero_documento:
            raise ValidationError("Error, El solicitante no puede ser igual al fallecido")

        if lugar_fallecimiento_tipo == 1:
            if hospital_id == 0:
                state_error = True

        if state_error:
            raise ValidationError("Error, Seleccione un hospital valido ")

    class Meta:
        model = Solicitud
        fields = '__all__'
        widgets = {
            'fallecido_fecha_nacimiento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fallecido_fecha_fallecimiento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_cremacion': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_necropsia': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_deposito': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'lugar_fallecimiento_direccion': Textarea(attrs={'rows': '3'}),
            'destino_cenizas': Textarea(attrs={'rows': '3'}),
            'solicitante_direccion': Textarea(attrs={'rows': '3'}),
        }


class SolicitudListFilter(gf.FilteredForm):
    es_covid = gf.ChoiceField(label=_('Causa de fallecimiento'), choices=(('True', _('Covid')),
                                                                          ('False', _('No Covid'))))

    fallecido_tipo_documento = gf.ChoiceField(label=_('Fallecido'),
                                              choices=(('1', 'D.N.I.'),
                                                       ('2', 'Carné de extrangería'),
                                                       ('3', 'Pasaporte'),
                                                       ('4', 'NN'),
                                                       ('6', 'C.I.'),
                                                       ('7', 'P.T.P.'),
                                                       ('8', 'Acta de nacimiento'),))

    solicitante_tipo_documento = gf.ChoiceField(label=_('Solicitante'),
                                                choices=(('1', 'D.N.I.'),
                                                         ('2', 'Carné de extrangería'),
                                                         ('3', 'Pasaporte'),
                                                         ('5', 'A.S.'),
                                                         ('6', 'C.I.'),
                                                         ('7', 'P.T.P.'),))

    def get_order_by_choices(self):
        return [('1', 'es_covid'), ('2', 'solicitante_tipo_documento'), ('3', 'fallecido_tipo_documento')]


class SolicitudListFilterDSAIA(gf.FilteredForm):
    es_covid = gf.ChoiceField(label=_('Causa de fallecimiento'), choices=(('True', _('Covid')),
                                                                          ('False', _('No Covid'))))

    estado = gf.ChoiceField(label=_('Estado'), choices=(('2', _('Registrado')),
                                                        ('4', _('Autorizado')),
                                                        ('5', _('Certificado'))))

    fallecido_tipo_documento = gf.ChoiceField(label=_('Fallecido'),
                                              choices=(('1', 'D.N.I.'),
                                                       ('2', 'Carné de extrangería'),
                                                       ('3', 'Pasaporte'),
                                                       ('4', 'NN'),
                                                       ('6', 'C.I.'),
                                                       ('7', 'P.T.P.'),
                                                       ('8', 'Acta de nacimiento'),))

    solicitante_tipo_documento = gf.ChoiceField(label=_('Solicitante'),
                                                choices=(('1', 'D.N.I.'),
                                                         ('2', 'Carné de extrangería'),
                                                         ('3', 'Pasaporte'),
                                                         ('5', 'A.S.'),
                                                         ('6', 'C.I.'),
                                                         ('7', 'P.T.P.'),))

    def get_order_by_choices(self):
        return [('1', 'es_covid'), ('2', 'estado'), ('3', 'solicitante_tipo_documento'),
                ('4', 'fallecido_tipo_documento')]


class SolicitudRegForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        lugar_fallecimiento_tipo = cleaned_data.get("lugar_fallecimiento_tipo")
        hospital_id = cleaned_data.get("hospital_id")
        state_error = False

        if lugar_fallecimiento_tipo == 1:
            if hospital_id == 0:
                state_error = True

        if state_error:
            raise ValidationError("Error, Seleccione un hospital valido ")

    class Meta:
        model = Solicitud
        fields = '__all__'
        widgets = {
            'fallecido_fecha_nacimiento': DateInput(format='%Y-%m-%d'),
            'fallecido_fecha_fallecimiento': DateInput(format='%Y-%m-%d'),
            'fecha_cremacion': DateInput(format='%Y-%m-%d'),
            'lugar_fallecimiento_direccion': Textarea(attrs={'rows': '3'}),
            'solicitante_direccion': Textarea(attrs={'rows': '3'}),
        }


class SolicitudFormSource(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['fallecido_parentesco'].choices = [('', '-- --')]

    class Meta:
        model = Solicitud
        fields = '__all__'
        widgets = {
            'fallecido_fecha_nacimiento': DateInput(format='%Y-%m-%d'),
            'fallecido_fecha_fallecimiento': DateInput(format='%Y-%m-%d'),
            'fecha_cremacion': DateInput(format='%Y-%m-%d'),
            'lugar_fallecimiento_direccion': Textarea(attrs={'rows': '3'}),
            'solicitante_direccion': Textarea(attrs={'rows': '3'}),
        }
