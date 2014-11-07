from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
    PasswordChangeForm, SetPasswordForm)
from django.forms import CharField


class LoginForm(AuthenticationForm):
    username = CharField()
    password = CharField()
