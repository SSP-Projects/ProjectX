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

#@login_required(login_url='/accounts/login/')
def home(request):

    json_serializer = serializers.get_serializer("json")()
    #companies = json_serializer.serialize(Company.objects.all().order_by('id')[:5], ensure_ascii=False)

    username = ""
    actual_employee =Employee.objects.get(user=request.user)
    workingStatus = actual_employee.work_status
    if workingStatus == "new":
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
    if request.is_ajax and request.method == "POST":
        actual_employee =Employee.objects.get(user=request.user)
        
        state = request.POST['state']
        interaction_type=request.POST['interaction_type']
        print("PRUEBARDA->"+request.POST['state'] )
        interaction=Interaction.objects.create(
        state=state,
        interaction_type=interaction_type,
        employee=actual_employee
        )
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
    else:
        return redirect("/home/")
       
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
    app_tittle = "SIGNET"
    return render(request, 'admin.html', context={'employees':employees, 'userForm' : userForm, "app_tittle":app_tittle,})


def getUser(request):
    if request.is_ajax and request.method == "GET":
        dni = request.GET['dni']
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
    userForm = forms.UserForm()

    return render(request, 'admin.html', context={'employees':employees, 'userForm' : userForm})
