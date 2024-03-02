from django import forms

from apps.localizations.models.country import Country
from apps.util.generic_filters import forms as gf


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class CountryListFilter(gf.FilteredForm):

    def get_order_by_choices(self):
        return []
