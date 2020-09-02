from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.conf import settings



class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Please enter email address")
        if not username:
            raise ValueError("Please enter username")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self,email,username,password):
        user = self.create_user(
                email=self.normalize_email(email),
                password = password,
                username = username,
             )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", unique=True)
    username = models.CharField(verbose_name="username", max_length=30)
    firstname = models.CharField(verbose_name="firstname", max_length=30)
    lastname = models.CharField(verbose_name="lastname", max_length=30)
    date_joined = models.DateTimeField(verbose_name="joindate", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="logindate", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_doctor = models.BooleanField('doctor status', default=False)
    is_patient = models.BooleanField('patient status', default=False)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = AccountManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True


class DoctorDepartment(models.Model):
    USER_CLINIC_CHOICES = (
        ("1", 'Neurology'),
        ("2",'Ear, Nose and Throat Disorders'),
        ("3", 'Diet and Nutrition'),
        ("4", 'Cardiology'),
        ("5", 'Psychology'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    department = models.CharField(choices=USER_CLINIC_CHOICES, max_length=100)
    

class Appointment(models.Model):
    old = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True, null=True,on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now=False, null=True, blank=True)
    time_start = models.TimeField(('start time'), blank=True, null=True)
    time_end =models.TimeField(('end time'), blank=True, null=True)
    appointment_with = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE)
    app_rate = models.IntegerField(default = 0)

class RateModel(models.Model):
    doctor = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE)
    rate = models.IntegerField(blank=True, default = 0)
    av_rate = models.IntegerField(blank=True, default = 0)