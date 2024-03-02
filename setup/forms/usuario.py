import os
import sys
if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    import django


from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UsernameField
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from apps.util.generic_filters import forms as gf
from setup.models.usuario import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        # fields = ['name',]
        widgets = {
            # 'password': DateInput(format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['groups'].choices = Group.objects.filter(name__in=['Administrador', 'Trabajador']).values_list('id',
        #                                                                                                            'name')
        self.fields['groups'].label = "Roles"
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

        user_permissions = self.fields.get('usuario_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(""),
    )

    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            # 'birthdate': DateInput(format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        # self.fields['groups'].choices = Group.objects.filter(name__in=['Administrador', 'Trabajador']).values_list(
        #     'id',
        #     'name')
        self.fields['groups'].label = "Roles"
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')


class UsuarioChangePasswordForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=(
            "La contraseña no puede asemejarse tanto a su otra información personal. La contraseña debe contener al menos 8 caracteres. La contraseña no puede ser una clave utilizada comunmente. La contraseña no puede ser completamente numérica."), )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Usuario
        fields = ("username", "is_active")
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UsuarioListFilter(gf.FilteredForm):
    # sex = gf.ChoiceField(label=_('Género'), choices=convert_choice_to_filter(SEXS))
    # civil_status = gf.ChoiceField(label=_('Estado civil'), choices=convert_choice_to_filter(CIVIL_STATUS))
    # degree_of_instruction = gf.ChoiceField(label=_('Grado de instrucción'), choices=convert_choice_to_filter(DEGRESS))

    def get_order_by_choices(self):
        return []
