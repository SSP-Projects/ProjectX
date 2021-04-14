from django import forms
from . import models

'''
class CenterForm(forms.ModelForm):
    class Meta:
        model = models.Center
        exclude = ['center_id', 'password_changed']
'''

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
