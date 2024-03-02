from django.contrib import admin
from django.contrib.auth.hashers import make_password

from setup.models.crematorio import Crematorio
from setup.models.entidad import Entidad
from setup.models.menu import Menu, GroupMenu
from setup.models.periodo import Periodo
from setup.models.token_validate_form import TokenValidateForm
from setup.models.usuario import Usuario


class UserModelAdmin(admin.ModelAdmin):
    """
        User for overriding the normal user admin panel, and add the extra fields added to the user
        """

    def save_model(self, request, obj, form, change):
        # user_database = Usuario.objects.get(pk=obj.pk)

        obj.password = make_password(obj.password)

        super().save_model(request, obj, form, change)


admin.site.register(Periodo)
admin.site.register(Usuario)
admin.site.register(Menu)
admin.site.register(GroupMenu)
admin.site.register(Entidad)
admin.site.register(Crematorio)
admin.site.register(TokenValidateForm)
