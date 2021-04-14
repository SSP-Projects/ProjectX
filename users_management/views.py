from django.shortcuts import render
from . import forms
from . models import Employee

def login(request):
    return render(request, 'login.html', context={})

def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form':form})

def home(request):
    return render(request, 'home.html', context={})

def admin(request):
    employees = Employee.objects.all()
    return render(request, 'admin.html', context={'employees':employees})