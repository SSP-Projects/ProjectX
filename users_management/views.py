from re import template
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.contrib.auth import authenticate, login
from . import forms
import json
from django.http import HttpResponse
from .models import Employee, Interaction, Notification, Center, NotificationTypesAuxiliar, User
from django.core import serializers
from django.contrib import messages 
from datetime import datetime, timedelta, date, time
from calendar import monthrange
from io import BytesIO
from xhtml2pdf import pisa
import smtplib
import base64
last_user = None

def login_view(request):
    app_tittle = "SIGNET"
    studycenter_name = "GMQ TECH"
    form = forms.LoginForm()
    correct_login = True

    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username.lower(), password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("/admin/")
        else:
            correct_login = False

    return render(request, 'login.html', context={
        'studycenter_name':studycenter_name,
        'app_tittle':app_tittle,
        'form': form,
        'correct_login':correct_login
    })

def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})
##HOME
@login_required(login_url='/login/')
def home(request):
    if request.user.is_staff:
        return redirect("/admin/")
    json_serializer = serializers.get_serializer("json")()
    #companies = json_serializer.serialize(Company.objects.all().order_by('id')[:5], ensure_ascii=False)

    actual_employee =Employee.objects.get(user=request.user)
    if actual_employee != None:
        username = ""
        workingStatus = actual_employee.work_status
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

def get_employee_job_interactions_date_range(request):
    if request.is_ajax:
        dni = request.GET['dni']
        start_date = request.GET['startDate']
        end_date = request.GET['endDate']
        user = Employee.objects.get(dni=dni)

        date_time_obj = datetime.strptime(end_date, '%Y-%m-%d')
        end_date_obj = date_time_obj + timedelta(days=1)


        employee_interactions = Interaction.objects.filter(employee = user, date_time__range=(start_date, end_date_obj)).order_by('-date_time')

        interactions_json = serializers.serialize('json',employee_interactions)
        return HttpResponse(interactions_json, content_type="application/json")
    return None


def get_employee_job_interactions_dni(request):

    if request.is_ajax:
        dni = request.GET['dni']
        user = Employee.objects.get(dni=dni)
        
        today = datetime.now() + timedelta(days=10000)
        starting_date = datetime.now() - timedelta(days=35)

        employee_interactions = Interaction.objects.filter(employee = user, date_time__range=(starting_date, today)).order_by('-date_time')

        interactions_json = serializers.serialize('json',employee_interactions)
        return HttpResponse(interactions_json, content_type="application/json")
    return None

def get_hours_from_range(request):
    
    if request.is_ajax:
        dni = request.GET['dni']
        date = request.GET['month_to_search']
        user = Employee.objects.get(dni=dni)
        date_month = datetime.strptime(date, "%Y-%m")
        next_month = (date_month + timedelta(days=32)).replace(day=1)

        employee_interactions = Interaction.objects.filter(employee = user, date_time__range=(date_month, next_month)).order_by('date_time')

        firstTime = None
        secondTime = None
        totalTime = 0
        for interaction in employee_interactions:
            print(interaction.interaction_type, " ", interaction.state, "-> ", interaction.date_time)
            if ((interaction.interaction_type == "work" and interaction.state == 0) or (interaction.interaction_type == "break" and interaction.state == 1)):
                firstTime = interaction.date_time
            elif ((interaction.interaction_type == "work" and interaction.state == 1) or (interaction.interaction_type == "break" and interaction.state == 0)):
                secondTime = interaction.date_time
            
            if (firstTime is not None and secondTime is not None):
                difference = secondTime - firstTime
                days, seconds = difference.days, difference.seconds
                hours = days * 24 + seconds // 3600
                minutes = minutes = (seconds % 3600) // 60
                hours += minutes / 60
                totalTime += hours
                firstTime = None
                secondTime = None
    formatted_hour = "{:.2f}".format(totalTime)
    return HttpResponse(json.dumps({"hours" : formatted_hour}), content_type="application/json")

def get_hours_from_current_month(request):
    if request.is_ajax:
        current_month = datetime.today().date().replace(day=1)
        next_month = (current_month + timedelta(days=32)).replace(day=1)
        user = Employee.objects.get(user=request.user)
        employee_interactions = Interaction.objects.filter(employee = user, date_time__range=(current_month, next_month)).order_by('date_time')
        daily_hours = {}
        firstTime = None
        secondTime = None
        for interaction in employee_interactions:
            if ((interaction.interaction_type == "work" and interaction.state == 0) or (interaction.interaction_type == "break" and interaction.state == 1)):
                firstTime = interaction.date_time
            elif ((interaction.interaction_type == "work" and interaction.state == 1) or (interaction.interaction_type == "break" and interaction.state == 0)):
                secondTime = interaction.date_time  
            if (firstTime is not None and secondTime is not None):
                difference = secondTime - firstTime
                days, seconds = difference.days, difference.seconds
                hours = days * 24 + seconds // 3600
                minutes = minutes = (seconds % 3600) // 60
                hours += minutes / 60
                try:
                    daily_hours[interaction.date_time.strftime("%d-%m-%Y")] += hours
                except:
                    daily_hours[interaction.date_time.strftime("%d-%m-%Y")] = hours
                firstTime = None
                secondTime = None
        for key in daily_hours.keys():
            daily_hours[key] = "{:.2f}".format(daily_hours[key])
        return HttpResponse(json.dumps(daily_hours), content_type="application/json")

def get_interactions_from_day(request):
    if request.is_ajax:
        day = request.GET['day']
        day_start = datetime.strptime(day, "%d-%m-%Y")
        day_end = day_start.replace(hour=23).replace(minute=59).replace(second=59)
        employee = Employee.objects.get(user = request.user)
        employee_interactions = Interaction.objects.filter(employee = employee, date_time__range=(day_start, day_end)).order_by('date_time')
        return HttpResponse(serializers.serialize('json',employee_interactions), content_type="application/json")


def send_email():
    gmail_user = 'help.ssp.projects@gmail.com'
    gmail_password = 'Pelirrojo64'

    sent_from = gmail_user
    to = ['garciamayosergio@gmail.com', 'sergio.munoz.lillo@gmail.com']
    subject = 'OMG Super Important Message'
    body = 'Hey, whats up?\n\n- You'
    email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
      
    print("Mensajes enviados!")

def get_employee_actual_status(request):
    actual_employee = Employee.objects.get(user=request.user)

    return HttpResponse(json.dumps({"employeeStatus":actual_employee.work_status}), content_type="application/json")
 
def getEmployeeInteractions(request):
    actual_employee = Employee.objects.get(user=request.user)
    if actual_employee != None:
        to_return = []
        days = {}
        #day-total_hours-details
        #type-hour
               
        employee_interactions = Interaction.objects.filter(employee = actual_employee).order_by('-date_time')
        #for interaction in employee_interactions:
        #    days[interaction.date_time.date()] 
        #get total hours ordered by day
        for interaction in employee_interactions:
            print(interaction.interaction_type, interaction.state) 
            try:
                days[str(interaction.date_time.date())].append(str(interaction.date_time.time())[:8])
            except:
                days[str(interaction.date_time.date())] = [str(interaction.date_time.time())[:8]]
        print(days)
        interactions_json = serializers.serialize('json', employee_interactions)

        return HttpResponse(interactions_json, content_type="application/json")
    return redirect("/")
    
def postInteraction(request):
    
    if request.is_ajax and request.method == "POST":
        actual_employee = Employee.objects.get(user=request.user)
        if actual_employee != None:
            today = datetime.now().date()
            tomorrow = today + timedelta(1)
            starting_date = datetime.combine(today, time())
            end_date =   datetime.combine(tomorrow, time())
            employee_interactions_count = Interaction.objects.filter(employee = actual_employee, interaction_type ="work",state=0, date_time__range=(starting_date, end_date)).count()
            interaction_type=request.POST['interaction_type']
            state = int(request.POST['state'])
            if (employee_interactions_count < 2 and interaction_type == "work" and state == 0) or state == 1 or interaction_type =="break":
               
                interaction=Interaction.objects.create(
                state=state,
                date_time=datetime.now(),
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
                print("INSERCION-> "+str(state)+str(interaction_type)+"/n"+"/n"+"/n"+"/n"+"/n")

                actual_employee.save()
                interaction.save()
                return HttpResponse(json.dumps({"a": "Penesito"}),  content_type="application/json")
            else:
                return HttpResponse(json.dumps({"error": "No se puede entrar al trabajo más de 2 veces al día"}),  content_type="application/json")

        
    return HttpResponse(405,"Ha ocurrido un error")
       
    # some error occured



@login_required(login_url='/login/')
def admin(request):
    if not request.user.is_staff:
        return redirect("/home/")
    form = forms.UserForm(request.POST or None, request.FILES or None)
    form_type = ''
    form_success = 'empty'

    if request.method == 'POST':
        
        if form.is_valid():

            formType = form.cleaned_data.get("form_type")
            name = form.cleaned_data.get('name').capitalize()
            surname = form.cleaned_data.get('surnames').capitalize()
            dni = form.cleaned_data.get('dni')
            ss = form.cleaned_data.get('ss_number')
            phone = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email').lower()
            signature = request.FILES['signature'] if 'signature' in request.FILES else False

            if formType == "Crear Usuario":
                if Employee.objects.filter(dni=dni).exists():
                    form_success = 'fail'
                    form_type = 'El DNI introducido ya existe'
                else:
                    center = Center.objects.get(CIF='A3424F23424')
                    user = User.objects.create_user(username=email, password=dni)
                    employee = Employee()
                    employee.name = name
                    employee.user = user
                    employee.dni = dni
                    employee.center = center
                    employee.surnames = surname
                    employee.ss_number = ss
                    employee.phone_number = phone
                    employee.email = email
                    employee.signature = signature
                    employee.professional_category = "Profesor"

                    user.save()
                    employee.save()
                    form_type = 'Usuario creado con éxito'
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
                employee.signature = signature
                user.username = email
                user.password = dni

                employee.save()
                user.save()
                form_type = 'Usuario editado con éxito'
            form_success = 'success'
        else:
            form_success = 'fail'
    
    employees = Employee.objects.filter(user__is_active = True)
    notification_types = NotificationTypesAuxiliar.objects.all()
    app_tittle = 'SIGNET'
    studycenter_name = 'GMQ TECH'

    return render(request, 'admin.html', context={
        'employees':employees,
        'studycenter_name':studycenter_name,
        'userForm' : form,
        'app_tittle':app_tittle,
        'notification_types': notification_types,
        'form_success': form_success,
        'form_type': form_type
    })
   
def get_pdf_from_month(request):
    def first_day_of_month(date):
        first_day = datetime(date.year, date.month, 1)
        return first_day.strftime('%Y-%m-%d')
    if request.is_ajax and request.method == "GET":
        #COMPROBAR SI HAY PERMISOS
        actual_employee = "Employee.objects.get(user=request.user)"
        if actual_employee != None:
            print("VCALOR QUE ME INTERESA-z>" +str(request.GET['month']))
            dni=request.GET['employee_dni']
            year =request.GET['month'].split("-")[0]
            month =request.GET['month'].split("-")[1]
            employee_to_download_register =Employee.objects.get(dni=dni)
            starting_date =  first_day_of_month(date(int(year), int(month), 1))
            end_date =   first_day_of_month(date(int(year),  int(month)+1, 1))

            employee_interactions = Interaction.objects.filter(employee = employee_to_download_register, date_time__range=(starting_date, end_date))
            encoded_string =None 
            with open( "./"+employee_to_download_register.signature.url, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            if len(employee_interactions) != 0:
                template = get_template('pdf/pdf_template.html')
                context_data = {
                "year":year,
                "month":month,
                "employee":employee_to_download_register,
                "employee_interactions":employee_interactions,
                "monthDays":range((date(int(year), int(month)+1, 1) - date(int(year), int(month), 1)).days+1),
                "signature":encoded_string
                }
                html  = template.render(context_data)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
                result.seek(0)
                if not pdf.err:
                    response = HttpResponse(result.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=' "Registro_jornada"+context_data["month"]+"/"+context_data["year"]+".pdf"
                    return response
            else:
                return HttpResponse({"error":"No interactions"}, content_type='application/json')
        else:
             return HttpResponse({"error":"illegal user"}, content_type='application/json')

def pdf_wuarron_testeo(request):
    def first_day_of_month(date):
        first_day = datetime(date.year, date.month, 1)
        return first_day.strftime('%Y-%m-%d')
    year = 2021
    month = 6
    starting_date =  first_day_of_month(date(int(year), int(month), 1))
    end_date =   first_day_of_month(date(int(year),  int(month)+1, 1))
    employee_interactions = Interaction.objects.filter(employee = Employee.objects.get(name="Manue"), date_time__range=(starting_date, end_date))
  
    encoded_string =None 
    with open( "./"+Employee.objects.get(name="Manue").signature.url, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    context_data = {
    "year":year,
    "month":month,
    "employee": Employee.objects.get(name="Manue"),
    "employee_interactions":employee_interactions,
    "monthDays":range((date(int(year), int(month)+1, 1) - date(int(year), int(month), 1)).days+1),
    "signature":encoded_string
    }
    return render(request, 'pdf/pdf_template.html', context=context_data)




def get_notifications_from_current_user(request):
    if request.is_ajax and request.method == "GET":
        to_return = []
        notifications = Notification.objects.filter(receiver=request.user)
        for notification in notifications:
            notif_id = notification.pk
            notif_date = notification.date_time.strftime("%H:%M %d-%m-%Y")
            notif_type = NotificationTypesAuxiliar.objects.get(pk=notification.notification_type).name
            to_return.append({
                'id': notif_id,
                'date': notif_date,
                'type': notif_type
            })
        return HttpResponse(json.dumps(to_return), content_type='application/json')
    return None

def get_notification_by_id(request):
    if request.is_ajax and request.method == "GET":
        notification = Notification.objects.get(pk=request.GET['id'])
        print()
        employee = Employee.objects.get(email=User.objects.get(pk=notification.sender.pk))
        to_return = {
            'notification': notification.pk,
            "sender": employee.pk,
            'sender_name': '(' + str(employee.dni) + ') ' + employee.name + ' ' + employee.surnames,
            'type': NotificationTypesAuxiliar.objects.get(pk=notification.notification_type).name,
            'desc': notification.description    
        }
        return HttpResponse(json.dumps(to_return), content_type='application/json')

def get_notification_by_id_user(request):
    if request.is_ajax and request.method == "GET":
        notification = Notification.objects.get(pk=request.GET['id'])
        to_return = {
            'notification': notification.pk,
            'type': NotificationTypesAuxiliar.objects.get(pk=notification.notification_type).name,
            'desc': notification.description    
        }
        return HttpResponse(json.dumps(to_return), content_type='application/json')

def set_notification_as_viewed(request):
    if request.is_ajax and request.method == "POST":
        Notification.objects.get(pk=request.POST['id']).delete()
        return HttpResponse(status=200)
    return HttpResponse(status=403)

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
        employee = Employee.objects.get(dni=dni)
        globals()['last_user'] = employee
        employees_json = json.loads(serializers.serialize('json', [ employee, ]))
        for employees in employees_json:
            employees["fields"]["is_active"] =User.objects.get(pk = employees["fields"]["user"]).is_active

        return HttpResponse(json.dumps(employees_json), content_type="application/json")
    return None
def get_users_by_name(request):
     if request.is_ajax and request.method == "GET":
        actual_employee =" Employee.objects.get(user=request.user)"
        if actual_employee != None:
            nameToSearch = request.GET['name']
            if nameToSearch == "":
                employees = Employee.objects.all().order_by('name')
            else:
                employees = Employee.objects.filter(name__contains = nameToSearch).order_by('name')

            employees_json = json.loads(serializers.serialize('json',employees))
            for employees in employees_json:
               employees["fields"]["is_active"] =User.objects.get(pk = employees["fields"]["user"]).is_active 

            return HttpResponse(json.dumps(employees_json), content_type="application/json")
        else:
            return HttpResponse(405)

def desactivate_user(request):
    if request.is_ajax and request.method == "POST":
        print(request.POST)
        dni = request.POST['dni']
        employee = Employee.objects.get(dni=dni)
        user = employee.user
        user.is_active = False
        user.save()
    return redirect('/admin/')

def activate_user(request):
    if request.is_ajax and request.method == "POST":
        print(request.POST)
        dni = request.POST['dni']
        employee = Employee.objects.get(dni=dni)
        user = employee.user
        user.is_active = True
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