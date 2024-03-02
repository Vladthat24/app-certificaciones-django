from rest_framework import routers

from setup.views_api.token_validate_form import TokenValidateFormRestViewSet
from setup.views_api.usuario import UsuarioRestViewSet

router = routers.DefaultRouter()
router.register(r'token-validate-form', TokenValidateFormRestViewSet)
router.register(r'usuarios', UsuarioRestViewSet)
