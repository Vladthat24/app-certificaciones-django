from django import forms
from django.forms import Textarea

from apps.solicitud.models.hospital import Hospital
from apps.util.generic_filters import forms as gf


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
        widgets = {
            'nombre_establecimiento': Textarea(attrs={'rows': '3'}),
            'direccion': Textarea(attrs={'rows': '3'}),
        }


class HospitalListFilter(gf.FilteredForm):
    def get_order_by_choices(self):
        return [('1', '')]
