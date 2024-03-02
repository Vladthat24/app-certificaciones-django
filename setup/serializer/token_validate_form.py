from rest_framework import serializers

from setup.models.token_validate_form import TokenValidateForm


class TokenValidateFormSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TokenValidateForm
        # fields = '__all__'
        fields = ['id', 'dominio', 'estado', 'token']
