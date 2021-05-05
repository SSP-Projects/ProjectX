from django import forms
from . import models


class CenterForm(forms.ModelForm):
    class Meta:
        model = models.Center
        exclude = ['center_id', 'password_changed']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.User
        exclude = ['user_id', 'password_changed']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = '__all__'

class SigningForm(forms.ModelForm):
    class Meta:
        model = models.Signing
        fields = '__all__'

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
class TicketForm(forms.Form):
    ticket_types =[("prueba1","prueba1_2"),("prueba2","prueba2_2")]
    ticket_type = forms.CharField(label="Seleccione el tipo de incidencia", widget=forms.Select(choices=ticket_types, attrs= 
        {
            'class': 'form-control text-center',
            'required': False,
            'id': 'ticket_type',
        }
       
    ))
    description = forms.CharField(label="Descripción del problema", max_length=600, widget=forms.Textarea(attrs=
        {
            'class': 'form-control no-resize',
            'required': False,
            'rows':"5",
            'id': 'description',
            'type': 'text'
        }
        
        
    ))

