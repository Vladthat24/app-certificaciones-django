from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from setup.models.token_validate_form import TokenValidateForm
from setup.serializer.token_validate_form import TokenValidateFormSerializer


class TokenValidateFormRestViewSet(viewsets.ModelViewSet):
    queryset = TokenValidateForm.objects.all()
    serializer_class = TokenValidateFormSerializer
    http_method_names = ['get', 'head']
    permission_classes = (AllowAny,)

    # permission_classes_by_action = {'create': [AllowAny],
    #                                 'list': [AllowAny]}

    def get_queryset(self):
        queryset = TokenValidateForm.objects.all()
        token = self.request.query_params.get('token', None)

        if token is not None:
            queryset = queryset.filter(token=token, estado=True)

        return queryset.distinct().order_by('-created_at')

    def perform_create(self, serializer):
        import secrets
        kwargs = {}
        kwargs['token'] = secrets.token_hex(25)[0:25]
        serializer.save(**kwargs)
