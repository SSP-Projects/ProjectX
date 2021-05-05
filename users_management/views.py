from django.shortcuts import render
from . import forms
from .models import Employee


def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

def home(request):
    username = ""
    form = forms.TicketForm()
    return render(request, 'middle/home.html', context={"studycenter_name":"GMQ CENTER","username":username,'form': form})

def admin(request):
    employees = Employee.objects.all()
    # employees[0].name = 'adawda'
    # employees[0].save()
    # employees = Employee.objects.get(name='oeoe')
    return render(request, 'admin.html', context={'employees':employees})
