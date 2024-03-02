from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.localizations.forms.country import CountryForm, CountryListFilter
from apps.localizations.models.country import Country
from apps.util.generic_filters.views import FilteredListView
from apps.util.views.dropdown_list import dropdown_list


class CountryList(FilteredListView):
    model = Country
    paginate_by = 10
    form_class = CountryListFilter
    filter_fields = []
    search_fields = ['name']
    default_order = '-id'

    def get_context_data(self, **kwargs):
        title = "Todas los paises"
        return dict(
            super(CountryList, self).get_context_data(**kwargs), title=title)


class CountryCreate(CreateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy('country:list')

    def form_valid(self, form):
        msg = "El país <strong>" + str(self.request.POST['name']) + "</strong>  fue creado correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)


class CountryUpdate(UpdateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy('country:list')

    def form_valid(self, form):
        msg = "El país <strong>" + str(self.request.POST['name']) + "</strong>  fue editado correctamente."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)


def dropdown_country(request):
    country_list = Country.objects.all()
    return dropdown_list(request=request, list=country_list)
