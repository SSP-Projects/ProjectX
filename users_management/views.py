from django.shortcuts import render
from . import forms
from . models import Employee

def login(request):
    form = forms.LoginForm()
    return render(request, 'login.html', context={'form': form})

def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

def home(request):
    return render(request, 'home.html', context={})

def admin(request):
    employees = Employee.objects.all()
    return render(request, 'admin.html', context={'employees':employees})