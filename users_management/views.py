from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Employee, Notification


def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

@login_required(login_url='/accounts/login/')
def home(request):
    username = ""
    app_tittle = "SIGNET"
    studycenter_name = "GMQ CENTER"
    form = forms.NotificationForm()
    return render(request, 'middle/home.html', context={"studycenter_name":studycenter_name,"app_tittle":app_tittle,"username":username,'form': form})

@login_required(login_url='/accounts/login/')
def admin(request):
    employees = Employee.objects.all()
    # employees[0].name = 'adawda'
    # employees[0].save()
    # employees = Employee.objects.get(name='oeoe')
    return render(request, 'admin.html', context={'employees':employees})

def send_notification(request):
    if request.method == 'POST':
        form = forms.NotificationForm(request.POST) 
        if form.is_valid():
            current_user = request.user
            notification = form.save(commit=False)
            notification.sender = request.user
            if not current_user.is_superuser:
                notification.receiver = request.user #TODO: get the admin of the system
            notification.save()