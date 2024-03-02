from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.localizations.views.country import CountryList, CountryCreate, CountryUpdate, dropdown_country
from apps.localizations.views.department import DepartmentList, DepartmentCreate, DepartmentUpdate, dropdown_department

app_name = 'country'

urlpatterns = [
    path('list', login_required(CountryList.as_view()), name='list'),
    path('new,', login_required(CountryCreate.as_view()), name='new'),
    path('edit/<pk>', login_required(CountryUpdate.as_view()), name='edit'),
    path('dropdown-list', login_required(dropdown_country), name='dropdown-list'),

    path('<country_id>/department/list', login_required(DepartmentList.as_view()), name='department-list'),
    path('<country_id>/department/new', login_required(DepartmentCreate.as_view()), name='department-new'),
    path('<country_id>/department/edit/<pk>', login_required(DepartmentUpdate.as_view()), name='department-edit'),
    path('department/dropdown-list', login_required(dropdown_department), name='department-dropdown-list'),

]
