from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Employee,Interaction, Center, User
from django.core import serializers


def register(request):
    form = forms.RegisterForm()
    return render(request, 'register.html', context={'form': form})

#@login_required(login_url='/accounts/login/')
def home(request):

    json_serializer = serializers.get_serializer("json")()
    #companies = json_serializer.serialize(Company.objects.all().order_by('id')[:5], ensure_ascii=False)

    username = ""
    workingStatus = "isntWorking"
    app_tittle = "SIGNET"
    studycenter_name = "GMQ CENTER"
    form = forms.TicketForm()
    return render(request, 'middle/home.html', context={
        "studycenter_name":studycenter_name,
        "app_tittle":app_tittle,
        "username":username,
        'form': form,
        "workingStatus": workingStatus
        
        })
def postInteraction(request):

    if request.is_ajax and request.method == "POST":


        ser_instance = serializers.serialize('json', [ instance, ])
        # send to client side.
        return JsonResponse({"instance": ser_instance}, status=200)


    # some error occured
    return JsonResponse({"error": ""}, status=400)


#@login_required(login_url='/accounts/login/')
def admin(request):

    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        
        if form.is_valid():

            formType = form.cleaned_data.get("form_type")
            print(formType)

            if formType == "Crear Usuario":

                name = form.cleaned_data.get('name')
                surname = form.cleaned_data.get('surnames')
                dni = form.cleaned_data.get('dni')
                ss = form.cleaned_data.get('ss_number')
                phone = form.cleaned_data.get('phone_number')
                email = form.cleaned_data.get('email')

                center = Center.objects.get(CIF='14231')
                user = User.objects.create_user(email, name, dni)

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
                form.save()
            return redirect('admin')
    
    employees = Employee.objects.all()
    userForm = forms.UserForm()

    return render(request, 'admin.html', context={'employees':employees, 'userForm' : userForm})
