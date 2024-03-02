from django.contrib.auth.decorators import login_required
from django.urls import path

from setup.views.usuario import UsuarioList, UsuarioCreate, UsuarioUpdate, UserPasswordUpdate

app_name = 'usuario'

urlpatterns = [
    path('list', login_required(UsuarioList.as_view()), name='list'),
    path('new', login_required(UsuarioCreate.as_view()), name='new'),
    path('edit/<pk>', login_required(UsuarioUpdate.as_view()), name='edit'),
    # path('delete/<pk>', login_required(PersonDelete.as_view()), name='delete'),
    # path('search', login_required(PersonSearch), name='search'),
    # path('all-json', login_required(person_all_json), name='all-json'),
    path('password/<pk>', login_required(UserPasswordUpdate.as_view()), name='password'),
]
