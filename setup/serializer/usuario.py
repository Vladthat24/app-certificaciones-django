from rest_framework import serializers

from setup.models.usuario import Usuario


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Usuario
        fields = '__all__'
