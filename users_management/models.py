from django.db import models
import uuid

class Center(models.Model):
    center_id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name             = models.CharField(max_length=50)
    address          = models.CharField(max_length=100)
    phone_number     = models.IntegerField()
    CIF              = models.CharField(max_length=9)
    email            = models.EmailField(max_length=50)
    image            = models.ImageField(blank=True)

class User(models.Model):
    class Permissions(models.IntegerChoices):
        EMPLOYEE     = 0
        CENTER       = 1
        ADMIN        = 2

    user_id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username         = models.CharField(max_length=50)
    password         = models.CharField(max_length=255)
    permission       = models.IntegerField(choices=Permissions.choices)
    center_id        = models.UUIDField(models.ForeignKey('Centers', on_delete=models.SET_NULL))
    password_changed = models.BooleanField(editable=False, default=False)
    image            = models.ImageField(blank=True)

class Employee(models.Model):
    employee_id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id          = models.UUIDField(models.ForeignKey('User', on_delete=models.SET_NULL))
    dni              = models.CharField(max_length=50)
    ss_number        = models.CharField(max_length=50)
    name             = models.CharField(max_length=50)
    surname          = models.CharField(max_length=50)
    phone_number     = models.IntegerField()
    email            = models.EmailField()

class Signing(models.Model):
    signing_id       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id      = models.UUIDField(models.ForeignKey('Employee', on_delete=models.SET_NULL))
    date             = models.DateField(auto_now_add=True)
    start_work       = models.TimeField(auto_now_add=True)
    start_rest       = models.TimeField(blank=True)
    end_rest         = models.TimeField(blank=True)
    end_work         = models.TimeField(blank=True)

