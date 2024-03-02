from django import forms
from django.forms import DateInput, Textarea
from django.utils.translation import ugettext_lazy as _

from apps.certificacion.models.certificacion import Certificacion, TIPOS
from apps.solicitud.models.solicitud import Solicitud
from apps.util.generic_filters import forms as gf


class CertificacionsModalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.solicitud = kwargs.pop('solicitud')
        super().__init__(*args, **kwargs)
        self.fields['solicitud'].choices = self.solicitud

    class Meta:
        model = Certificacion
        fields = '__all__'
        widgets = {
            'fallecido_fecha': DateInput(format='%Y-%m-%d'),
            'fecha_cert_necropsia': DateInput(format='%Y-%m-%d'),
            'fecha_recepcion': DateInput(format='%Y-%m-%d'),
            'motivo': Textarea(attrs={'rows': '3'}),
            'tipo_otro': Textarea(attrs={'rows': '3'}),
            'solicitante': Textarea(attrs={'rows': '3'}),
            'fallecido_nombre': Textarea(attrs={'rows': '3'}),
            'fallecido_direccion': Textarea(attrs={'rows': '3'}),
            'necropsia_causa_muerte': Textarea(attrs={'rows': '3'}),
            'necropsia_numero': Textarea(attrs={'rows': '3'}),
        }


class CertificacionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['solicitud'].choices = Solicitud.objects.filter(pk=-1).values_list('id',
                                                                                       'solicitante_numero_documento')

        self.fields['tipo'].choices = TIPOS[1:]

    class Meta:
        model = Certificacion
        fields = '__all__'
        widgets = {
            'fecha_recepcion': DateInput(format='%Y-%m-%d'),
            'motivo': Textarea(attrs={'rows': '3'}),
            'tipo_otro': Textarea(attrs={'rows': '3'}),
            'solicitante': Textarea(attrs={'rows': '3'}),
            'fallecido_nombre': Textarea(attrs={'rows': '3'}),
            'fallecido_direccion': Textarea(attrs={'rows': '3'}),
            'necropsia_causa_muerte': Textarea(attrs={'rows': '3'}),
            'necropsia_numero': Textarea(attrs={'rows': '3'}),
            'fallecido_fecha': DateInput(format='%Y-%m-%d'),
            'fecha_cert_necropsia': DateInput(format='%Y-%m-%d'),
        }


class CertificacionsUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo')
        solicitud = kwargs.pop('solicitud')
        super().__init__(*args, **kwargs)
        self.fields['solicitud'].choices = Solicitud.objects.filter(pk=solicitud).values_list('id',
                                                                                       'solicitante_numero_documento')

        if tipo == 1:
            self.fields['tipo'].choices = TIPOS[0:1]
        else:
            self.fields['tipo'].choices = TIPOS[1:]

    class Meta:
        model = Certificacion
        fields = '__all__'
        widgets = {
            'fecha_recepcion': DateInput(format='%Y-%m-%d'),
            'motivo': Textarea(attrs={'rows': '3'}),
            'tipo_otro': Textarea(attrs={'rows': '3'}),
            'solicitante': Textarea(attrs={'rows': '3'}),
            'fallecido_nombre': Textarea(attrs={'rows': '3'}),
            'fallecido_direccion': Textarea(attrs={'rows': '3'}),
            'necropsia_causa_muerte': Textarea(attrs={'rows': '3'}),
            'necropsia_numero': Textarea(attrs={'rows': '3'}),
            'fallecido_fecha': DateInput(format='%Y-%m-%d'),
            'fecha_cert_necropsia': DateInput(format='%Y-%m-%d'),
        }


class CertificacionsListFilter(gf.FilteredForm):
    solicitud__es_covid = gf.ChoiceField(label=_('Causa de fallecimiento'), choices=(('True', _('Covid')),
                                                                                     ('False', _('No Covid'))))

    def get_order_by_choices(self):
        return [('1', 'solicitud__es_covid')]


#
class CertificacionsModal2Form(forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = '__all__'
