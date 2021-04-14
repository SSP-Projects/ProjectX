from django.shortcuts import render
from . import forms

def login(request):
    return render(request, 'login.html', context={})

def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form':form})

def home(request):
    return render(request, 'home.html', context={})