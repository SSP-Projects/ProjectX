from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . import forms
import json
from .models import Employee, Interaction, Notification
from django.core import serializers



def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

@login_required(login_url='/accounts/login/')
def home(request):

    json_serializer = serializers.get_serializer("json")()
    #companies = json_serializer.serialize(Company.objects.all().order_by('id')[:5], ensure_ascii=False)

    username = ""
    workingStatus = "isntWorking"
    app_tittle = "SIGNET"
    studycenter_name = "GMQ CENTER"

    form = forms.NotificationForm()
    return render(request, 'middle/home.html', context={
        "studycenter_name":studycenter_name,
        "app_tittle":app_tittle,
        "username":username,
        'form': form,
        "workingStatus": workingStatus
        
        })

def postInteraction(request):
    print("dfishbfihdbufijbsfijku")
    if request.is_ajax and request.method == "POST":
        actual_employee =Employee.objects.get(user=request.user)
        print("PRUEBARDA->"+request.POST['state'] )
        interaction=Interaction.objects.create(
        state=request.POST['state'],
        interaction_type=request.POST['interaction_type'],
        employee=actual_employee
        )

        interaction.save()
        return redirect("/home/")
    else:
        return redirect("/home/")
       
    # some error occured


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