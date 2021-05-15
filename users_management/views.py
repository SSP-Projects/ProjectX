from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Employee,Interaction
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
    employees = Employee.objects.all()
    # employees[0].name = 'adawda'
    # employees[0].save()
    # employees = Employee.objects.get(name='oeoe')
    return render(request, 'admin.html', context={'employees':employees})
