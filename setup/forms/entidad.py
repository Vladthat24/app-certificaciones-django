from django import forms

from apps.util.generic_filters import forms as gf
from setup.models.entidad import Entidad


class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad
        fields = '__all__'


class EntidadListFilter(gf.FilteredForm):

    def get_order_by_choices(self):
        return []
