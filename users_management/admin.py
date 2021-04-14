from django.contrib import admin
from .models import User, Employee, Signing #, Center


# admin.site.register(Center)
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Signing)