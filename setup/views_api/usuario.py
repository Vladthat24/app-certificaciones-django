from rest_framework import viewsets

from setup.models.usuario import Usuario
from setup.serializer.usuario import UsuarioSerializer


class UsuarioRestViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
