from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . import forms
import json
from django.http import HttpResponse
from .models import Employee, Interaction, Notification, Center, User
from django.core import serializers

last_user = None

def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

@login_required(login_url='/accounts/login/')
def home(request):


    actual_employee =Employee.objects.get(user=request.user)
    if actual_employee != None:
        username = ""
        workingStatus = actual_employee.work_status
        if workingStatus == "new":
            workingStatus = "isntWorking" 
        app_tittle = "SIGNET"
        studycenter_name = "GMQ TECH"

        form = forms.NotificationForm()
        return render(request, 'middle/home.html', context={
            "studycenter_name":studycenter_name,
            "app_tittle":app_tittle,
            "username":username,
            'form': form,
            "workingStatus": workingStatus
            
            })
    return redirect("/")


def getEmployeeInteractions(request):

    actual_employee = Employee.objects.get(user=request.user)
    if actual_employee != None:
        employee_interactions = Interaction.objects.filter(employee = actual_employee).order_by('-date_time')
        interactions_json = serializers.serialize('json',employee_interactions)
        return HttpResponse(interactions_json, content_type="application/json")
    return redirect("/")
    
def postInteraction(request):
    
    if request.is_ajax and request.method == "POST":
        actual_employee = Employee.objects.get(user=request.user)
        if actual_employee != None:
            state = request.POST['state']
            interaction_type=request.POST['interaction_type']
            print("PRUEBARDA->"+request.POST['state'] )
            interaction=Interaction.objects.create(
            state=state,
            interaction_type=interaction_type,
            employee=actual_employee
            )
    
            state = int(state)    
            if interaction_type == "work" and state == 0:
                actual_employee.work_status ="isWorking"
            if interaction_type == "work" and state == 1:
                actual_employee.work_status ="isntWorking"
            if interaction_type == "break" and state == 0:
                actual_employee.work_status ="breaking"
            if interaction_type == "break" and state == 1:
                actual_employee.work_status ="isWorking"

            actual_employee.save()
            interaction.save()
            return redirect("/home/")
        
    return redirect("/")
       
    # some error occured



#@login_required(login_url='/accounts/login/')
def admin(request):

    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        
        if form.is_valid():

            formType = form.cleaned_data.get("form_type")
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surnames')
            dni = form.cleaned_data.get('dni')
            ss = form.cleaned_data.get('ss_number')
            phone = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')

            if formType == "Crear Usuario":

                center = Center.objects.get(CIF='A3424F23424')
                user = User.objects.create_user(email, email, dni)
                employee = Employee()
                employee.name = name
                employee.user = user
                employee.dni = dni
                employee.center_id = center
                employee.surnames = surname
                employee.ss_number = ss
                employee.phone_number = phone
                employee.email = email
                employee.professional_category = "Profesor"
                
                user.save()
                employee.save()
            else:
                employee = Employee.objects.get(dni=last_user.dni)
                user = User.objects.get(username=last_user.email)

                employee.name = name
                employee.user = user
                employee.dni = dni
                employee.surnames = surname
                employee.ss_number = ss
                employee.phone_number = phone
                employee.email = email

                user.username = email
                user.password = dni

                employee.save()
                user.save()


            return redirect('admin')
    
    employees = Employee.objects.all()
    userForm = forms.UserForm()
    app_tittle = 'SIGNET'
    studycenter_name = 'GMQ TECH'
    return render(request, 'admin.html', context={
        'employees':employees,
        'studycenter_name':studycenter_name,
        'userForm' : userForm,
        'app_tittle':app_tittle,
        })


def getUser(request):
    if request.is_ajax and request.method == "GET":
        dni = request.GET['dni']
        print(dni)
        user = Employee.objects.get(dni=dni)
        globals()['last_user'] = user
        userJson = serializers.serialize('json', [ user, ])
        return HttpResponse(userJson, content_type="application/json")
    return None

def delete_user(request):
    if request.is_ajax and request.method == "POST":
        dni = request.POST['dni']
        employee = Employee.objects.get(dni=dni)
        user = employee.user
        user.is_active = False
        user.save()
    return redirect('/admin/')


def staff_send_notification(request):
    if request.is_ajax and request.method == "POST":
        current_user = request.user
        dnis = request.POST['dnis']
        notification_type = request.POST['not_type']
        notification_desc = request.POST['not_desc']
        for dni in dnis:
            a = Notification()
            a.sender = current_user
            a.receiver = Employee.objects.get(dni=dni)
            a.notification_type = notification_type
            a.description = notification_desc
            a.save()
    return HttpResponse(code=200)

def send_notification(request):
    if request.is_ajax and request.method == "POST":
        current_user = request.user
        admins = Employee.objects.filter(is_staff=True)
        notification_type = request.POST['not_type']
        notification_desc = request.POST['not_desc']
        for admin in admins:
            a = Notification()
            a.sender = current_user
            a.receiver = admin
            a.notification_type = notification_type
            a.description = notification_desc
            a.save()
    return HttpResponse(code=200)
