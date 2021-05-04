from django.shortcuts import render
from . import forms
from . models import Employee


def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

def home(request):
    username = ""
    return render(request, 'middle/home.html', context={"studycenter_name":"GMQ CENTER","username":username})

def admin(request):
    employees = Employee.objects.all()
    return render(request, 'admin.html', context={'employees':employees})
