from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.localizations.views.district import get_district_by_id, get_district_autocomplete, dropdown_district

app_name = 'district'

urlpatterns = [
    path('json/<pk>', login_required(get_district_by_id), name='get-json'),
    path('json', get_district_autocomplete, name='json'),
    path('dropdown', dropdown_district, name='dropdown'),
]
