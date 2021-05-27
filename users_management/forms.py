from django import forms
from .models import Employee
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

class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        exclude = ['sender', 'receiver']

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        notification_types = models.NotificationTypesAuxiliar.objects.all()
        notification_types_titles = [(notification_type.id, notification_type.name) for notification_type in notification_types]
        self.fields['notification_type'].widget = forms.Select(
            choices=notification_types_titles, 
            attrs= {
                'class': 'form-control text-center',
                'required': True,
                'id': 'ticket_type'
            }
        )
        self.fields['notification_type'].label = 'Tipo de notificación'
        self.fields['description'].widget=forms.Textarea(attrs={
            'class': 'form-control no-resize',
            'required': False,
            'rows':"5",
            'id': 'ticket_description'
        })     
        self.fields['description'].label = 'Descripción'

class UserForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['dni', 'ss_number', 'phone_number', 'email', 'name', 'surnames']

    form_type = forms.CharField( widget=forms.HiddenInput(attrs=
        {
            'id': 'type',
            'class': 'form-control',
            'type': 'hidden'
        }
    ))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            

