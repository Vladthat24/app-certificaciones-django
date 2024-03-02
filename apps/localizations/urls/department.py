from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.localizations.views.province import ProvinceList, ProvinceCreate, ProvinceUpdate, dropdown_province

app_name = 'department'

urlpatterns = [

    path('<department_id>/province/list', login_required(ProvinceList.as_view()), name='province-list'),
    path('<department_id>/province/new', login_required(ProvinceCreate.as_view()), name='province-new'),
    path('<department_id>/province/edit/<pk>', login_required(ProvinceUpdate.as_view()), name='province-edit'),
    path('province/dropdown-list', login_required(dropdown_province), name='province-dropdown-list'),

]
