from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.solicitud.views.hospital import hospital_all_json, hospital_filter_json, HospitalList, HospitalCreate, \
    HospitalUpdate

app_name = 'hospital'

urlpatterns = [

    path('list', login_required(HospitalList.as_view()), name='list'),
    path('new', login_required(HospitalCreate.as_view()), name='new'),
    path('edit/<pk>', login_required(HospitalUpdate.as_view()), name='edit'),
    path('all-json', login_required(hospital_all_json), name='all-json'),
    path('filter-json', login_required(hospital_filter_json), name='filter-json'),

]
