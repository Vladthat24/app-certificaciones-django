from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.localizations.views.district import DistrictList, DistrictCreate, DistrictUpdate, dropdown_district
from apps.localizations.views.province import dropdown_province

app_name = 'province'

urlpatterns = [
    path('dropdown', dropdown_province, name='dropdown'),
    path('<province_id>/district/list', login_required(DistrictList.as_view()), name='district-list'),
    path('<province_id>/district/new', login_required(DistrictCreate.as_view()), name='district-new'),
    path('<province_id>/district/edit/<pk>', login_required(DistrictUpdate.as_view()), name='district-edit'),
    path('district/dropdown-list', login_required(dropdown_district), name='district-dropdown-list'),

]
