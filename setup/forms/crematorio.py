from django import forms
from django.forms import Textarea

from apps.util.generic_filters import forms as gf
from setup.models.crematorio import Crematorio


class CrematorioForm(forms.ModelForm):
    class Meta:
        model = Crematorio
        fields = '__all__'
        widgets = {
            'direccion': Textarea(attrs={'rows': '3'}),
            'nombre': Textarea(attrs={'rows': '3'}),
        }


class CrematorioListFilter(gf.FilteredForm):

    def get_order_by_choices(self):
        return []
