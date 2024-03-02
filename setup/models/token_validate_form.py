from django.db import models

from apps.middlewares.request import AppRequestMiddleware
from apps.util.network import get_client_ip
from setup.models.usuario import Usuario


class TokenValidateForm(models.Model):
    # Body
    dominio = models.CharField('Dominio', max_length=150)
    estado = models.BooleanField('Estado', default=True)
    token = models.CharField('Token', max_length=25)

    # Auditoria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_ip = models.CharField(max_length=20, null=True, blank=True)
    updated_ip = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.ForeignKey(Usuario, related_name='users_created', null=True, blank=True,
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(Usuario, related_name='users_updated', null=True, blank=True,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return " %s - %s " % (self.dominio, self.token)

    def save(self, *args, **kwargs):
        current_request = AppRequestMiddleware.get_request()
        u = current_request.user

        if self.pk:
            self.updated_ip = get_client_ip(current_request)
            if not u.is_anonymous:
                self.updated_by = u
        else:
            if not u.is_anonymous:
                self.created_by = u
                self.updated_by = u
            self.created_ip = get_client_ip(current_request)
            self.updated_ip = get_client_ip(current_request)

        super(TokenValidateForm, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Token Validate Form'
        verbose_name_plural = 'Token Validate Form'
