from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserFormBase(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_email': _('A user with that email address already exists.'),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        help_text=_('Enter the same password as above, for verification.'),
    )

    class Meta:
        model = User

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data['email']
        qs = User._default_manager
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        try:
            qs.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.errors['password2'] = self.error_class([self.error_messages['password_mismatch']])
            self.errors['password1'] = self.error_class([self.error_messages['password_mismatch']])
            del cleaned_data['password2']
            del cleaned_data['password1']

        return cleaned_data

    def save(self, commit=True):
        user = super(UserFormBase, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserCreateForm(UserFormBase):
    class Meta(UserFormBase.Meta):
        fields = ('email', 'name')


class UserEditForm(UserFormBase):
    class Meta(UserFormBase.Meta):
        fields = ('email', 'name')

    def __init__(self, *args, **kwargs):
        super(UserFormBase, self).__init__(*args, **kwargs)
        self.fields['password2'].required = False
        self.fields['password1'].required = False
