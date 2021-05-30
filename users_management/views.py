from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . import forms
import json
from django.http import HttpResponse
from .models import Employee, Interaction, Notification, Center, NotificationTypesAuxiliar, User
from django.core import serializers
from datetime import datetime, timedelta


last_user = None

def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

@login_required(login_url='/accounts/login/')
def home(request):
    if request.user.is_staff:
        return redirect("/admin/")
    json_serializer = serializers.get_serializer("json")()
    #companies = json_serializer.serialize(Company.objects.all().order_by('id')[:5], ensure_ascii=False)

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

def get_employee_job_interactions_dni(request):
    if request.is_ajax:
        dni = request.GET['dni']
        user = Employee.objects.get(dni=dni)
        
        today = datetime.now()
        starting_date = datetime.now() - timedelta(days=35)

        employee_interactions = Interaction.objects.filter(employee = user, date_time__range=(starting_date, today)).order_by('-date_time')

        interactions_json = serializers.serialize('json',employee_interactions)
        return HttpResponse(interactions_json, content_type="application/json")
    return None

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
            interaction=Interaction.objects.create(
            state=state,
            date_time=datetime.now(),
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



@login_required(login_url='/accounts/login/')
def admin(request):
    if not request.user.is_staff:
        return redirect("/home/")

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
                employee.center = center
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
    
    employees = Employee.objects.filter(user__is_active = True)
    userForm = forms.UserForm()
    notification_types = NotificationTypesAuxiliar.objects.all()
    app_tittle = 'SIGNET'
    studycenter_name = 'GMQ TECH'

    

    return render(request, 'admin.html', context={
        'employees':employees,
        'studycenter_name':studycenter_name,
        'userForm' : userForm,
        'app_tittle':app_tittle,
        'notification_types': notification_types,
    })

def get_notifications_from_current_user(request):
    if request.is_ajax and request.method == "POST":
        to_return = []
        notifications = Notification.objects.filter(receiver=request.user)
        for notification in notifications:
            notif_sender = notification.sender.username
            notif_date = notification.date_time.strftime("%H:%M %d-%m-%Y")
            notif_type = NotificationTypesAuxiliar.objects.get(pk=notification.notification_type).name
            notif_desc = notification.description
            to_return.append({
                'sender':notif_sender,
                'date': notif_date,
                'type': notif_type,
                'description': notif_desc
            })
        return HttpResponse(json.dumps(to_return), content_type='application/json')
    return None


def modifyInteraction(request):
    if request.is_ajax and request.method == "POST":
        changeType = request.POST['type']
        key = request.POST['key']
        newvalue = request.POST['value']
       
        interaction = Interaction.objects.get(pk=key);
        old_date = interaction.date_time.strftime("%m-%d-%Y %H:%M:%S+00:00")
        if (changeType == 'time'):
            old_time = old_date[11:19]
            print("old", old_time)
            print("new", newvalue)
            new_date = datetime.strptime(old_date.replace(old_time, newvalue), "%m-%d-%Y %H:%M:%S+00:00")
            interaction.date_time = new_date
        else:
            new_string = newvalue[5:7] + "-" + newvalue[8:10] + "-" + newvalue[0:4]
            old_string = old_date[0:10]
            new_date = datetime.strptime(old_date.replace(old_string, new_string), "%m-%d-%Y %H:%M:%S+00:00")
            interaction.date_time = new_date
            
        interaction.save()

        return HttpResponse(status=200)
    return HttpResponse(status=403)

def getUser(request):
    if request.is_ajax and request.method == "GET":
        dni = request.GET['dni']
        user = Employee.objects.get(dni=dni)
        globals()['last_user'] = user
        userJson = serializers.serialize('json', [ user, ])
        return HttpResponse(userJson, content_type="application/json")
    return None
def get_users_by_name(request):
     if request.is_ajax and request.method == "GET":
        actual_employee =" Employee.objects.get(user=request.user)"
        if actual_employee != None:
            nameToSearch = request.GET['name']
            if nameToSearch == "":
                employees = Employee.objects.all()
            else:
                employees = Employee.objects.filter(name__contains = nameToSearch)
            employees_json = serializers.serialize('json',employees)
            return HttpResponse(employees_json, content_type="application/json")
        else:
            return HttpResponse(405)

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
        dnis = request.POST.getlist('dnis[]')
        notification_type = request.POST['notification_type']
        notification_desc = request.POST['notification_desc']
        for dni in dnis:
            a = Notification()
            a.sender = current_user
            b = Employee.objects.get(dni=dni)
            a.receiver = b.user
            a.notification_type = notification_type
            a.description = notification_desc
            a.save()
    return redirect('/admin/')

def send_notification(request):
    if request.is_ajax and request.method == "POST":
        current_user = request.user
        admins = User.objects.filter(is_staff=True)
        notification_type = request.POST['notification_type']
        notification_desc = request.POST['notification_desc']
        for admin in admins:
            a = Notification()
            a.sender = current_user
            a.receiver = admin
            a.notification_type = notification_type
            a.description = notification_desc
            a.save()
    return redirect('/home/')
