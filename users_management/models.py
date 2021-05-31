from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid
from datetime import datetime, timedelta

# AUX TABLES

class PermissionsAuxiliar(models.Model):
    name = models.CharField(max_length=20)

class WeekDaysAuxiliar(models.Model):
    name = models.CharField(max_length=9)

class ProfessionalCategoryAuxiliar(models.Model):
    name = models.CharField(max_length=20)

class InteractionsTypesAuxiliar(models.Model):
    name = models.CharField(max_length=20)

class NotificationTypesAuxiliar(models.Model):
    name = models.CharField(max_length=50)

# END AUX TABLES

class Center(models.Model):
    center_id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name                  = models.CharField(max_length=50)
    address               = models.CharField(max_length=100)
    phone_number          = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,10}$')])
    CIF                   = models.CharField(max_length=9)
    email                 = models.EmailField(max_length=50)
    image                 = models.ImageField(blank=True)

class Employee(models.Model):
    user                  = models.OneToOneField(User, on_delete=models.CASCADE)
    center                = models.ForeignKey(Center, on_delete=models.CASCADE)
    dni                   = models.CharField(max_length=9)
    ss_number             = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{1,10}$')])
    professional_category = models.CharField(max_length=20) 
    signature             = models.ImageField(blank=True)
    phone_number          = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,10}$')])
    email                 = models.EmailField()
    name                  = models.CharField(max_length=30)
    surnames              = models.CharField(max_length=120)
    work_status           = models.CharField(max_length=20, default="new")

class Notification(models.Model):
    sender                = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver              = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    notification_type     = models.CharField(max_length=50)
    description           = models.CharField(max_length=500)
    date_time             = models.DateTimeField(auto_now=True)
    viewed                = models.BooleanField(default=False)

class Schedule(models.Model):
    entry_time            = models.TimeField()
    exit_time             = models.TimeField()
    weekday               = models.CharField(max_length=9)
    employee              = models.ForeignKey(Employee, on_delete=models.CASCADE)  

class Interaction(models.Model):
    class States(models.IntegerChoices):
        ENTER = 0
        EXIT  = 1
    date_time             = models.DateTimeField()
    state                 = models.IntegerField(choices=States.choices)
    interaction_type      = models.CharField(max_length=20)
    employee              = models.ForeignKey(Employee, on_delete=models.CASCADE)