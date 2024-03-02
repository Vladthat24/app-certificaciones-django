from django import forms

from apps.localizations.models.province import Province
from apps.util.generic_filters import forms as gf


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = '__all__'


class ProvinceListFilter(gf.FilteredForm):

    def get_order_by_choices(self):
        return []
