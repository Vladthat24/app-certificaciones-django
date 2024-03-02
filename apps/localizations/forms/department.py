from django import forms

from apps.localizations.models.department import Department
from apps.util.generic_filters import forms as gf


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentListFilter(gf.FilteredForm):

    def get_order_by_choices(self):
        return []
