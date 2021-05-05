from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Employee


def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

@login_required(login_url='/accounts/login/')
def home(request):
    username = ""
    form = forms.TicketForm()
    return render(request, 'middle/home.html', context={"studycenter_name":"GMQ CENTER","username":username,'form': form})

@login_required(login_url='/accounts/login/')
def admin(request):
    employees = Employee.objects.all()
    # employees[0].name = 'adawda'
    # employees[0].save()
    # employees = Employee.objects.get(name='oeoe')
    return render(request, 'admin.html', context={'employees':employees})
