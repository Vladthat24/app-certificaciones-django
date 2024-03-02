from django import forms

from apps.localizations.models.district import District
from apps.util.generic_filters import forms as gf


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'


class DistrictListFilter(gf.FilteredForm):

    def get_order_by_choices(self):
        return []
