from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Employee


def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

#@login_required(login_url='/accounts/login/')
def home(request):
    username = ""
    app_tittle = "SIGNET"
    studycenter_name = "GMQ CENTER"
    form = forms.TicketForm()
    return render(request, 'middle/home.html', context={"studycenter_name":studycenter_name,"app_tittle":app_tittle,"username":username,'form': form})

#@login_required(login_url='/accounts/login/')
def admin(request):
    employees = Employee.objects.all()
    # employees[0].name = 'adawda'
    # employees[0].save()
    # employees = Employee.objects.get(name='oeoe')
    return render(request, 'admin.html', context={'employees':employees})
