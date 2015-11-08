"""
Forms for the Player model
"""

import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

PASSWORD_MAXLENGTH = 60

class LoginForm(forms.Form):
    """
    Form view class for rendering the login form
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'required': True, 'class': 'form-control'}
        ),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'required': True, 'max_length': PASSWORD_MAXLENGTH, 'render_value':False, 'class': 'form-control'}
        ),
        label=_("Password")
    )


class RegistrationForm(forms.Form):
    """
    Form view class for rendering the registration form
    """

    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs={'required': True, 'max_length': 30, 'class': 'form-control'}),
        label=("Username"),
        error_messages={
            'invalid': (
                "This value must contain only letters, numbers and underscores."
            )
        }
    )

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': True,
        'max_length': PASSWORD_MAXLENGTH,
        'render_value': False,
        'class': 'form-control',
    }), label=_("Password"))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': True,
        'max_length': PASSWORD_MAXLENGTH,
        'render_value': False,
        'class': 'form-control',
    }), label=_("Password (again)"))

    def clean_username(self):
        """
        Check whether username has already been user
        """

        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        """
        Make sure both the password fields matched
        """

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
