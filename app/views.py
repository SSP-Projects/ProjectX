from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'login.html', context={})

def user(request):
    return render(request, 'user.html', context={})

def admin(request):
    # AQUÍ SE DEBE HACER EL PROCESO DE SACAR TODOS LOS EMPLEADOS
    return render(request, 'admin.html', context={})

def register(request):
    return render(request, 'register.html', context={})