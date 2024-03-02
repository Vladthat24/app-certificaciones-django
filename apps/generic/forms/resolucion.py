from django import forms

from apps.generic.models.resolucion import Resolucion
from apps.util.generic_filters import forms as gf


class ResolucionForm(forms.ModelForm):
    class Meta:
        model = Resolucion
        fields = '__all__'


class ResolucionListFilter(gf.FilteredForm):

    def get_order_by_choices(self):
        return []
