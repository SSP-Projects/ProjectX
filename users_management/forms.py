from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs=
        {
            'class': 'form-control',
            'id': 'username',
            'type': 'text'
        }
    ))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs=
        {
            'class': 'form-control',
            'id': 'password',
            'type': 'password'
        }
    ))
    sign_on_login = forms.BooleanField(widget=forms.CheckboxInput(attrs=
        {
            'class': 'form-check-input',
            'id': 'sign_on_login',
            'type': 'checkbox'
        }
    ))
