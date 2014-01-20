from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .forms import UserFormBase
from .models import User


class UserCreationForm(UserFormBase):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    pass

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
