from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class AuthProfileManager(BaseUserManager):

    def create_user(self, username, role, mobile, password=None):
        if not username:
            raise ValueError('User must have an username address')

        user = self.model(username=username)
        user.role = role
        user.mobile = mobile
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, role, mobile, password):
        user = self.create_user(username, role, mobile, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class AuthProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    objects = AuthProfileManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Patient(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)


class Doctor(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    spec = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    online_pay = models.BooleanField()
    experience_years = models.IntegerField()
    address = models.CharField(max_length=1023)
    avg_score = models.IntegerField(blank=True, null=True)
    first_empty_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=255)
    week_days = ArrayField(models.BooleanField(blank=True), size=7, )

    def __str__(self):
        return self.name + "-" + self.spec


class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    commenter = models.CharField(max_length=1023)
    reason = models.CharField(max_length=255)
    score = models.IntegerField()
    text = models.CharField(max_length=1023)
    # patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)


class Reserve(models.Model):
    date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
