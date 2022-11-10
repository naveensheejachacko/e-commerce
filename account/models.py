from email.policy import default
from tabnanny import verbose
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib import messages
import random





# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,first_name,last_name,phone_number,password=None):
        if not email:
            raise ValueError('email required')
        if not username:
            raise ValueError('username required')   
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        ) 
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password,first_name,last_name,phone_number):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name="email",max_length=60,unique=True)
    username=models.CharField(max_length=30,unique=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone_number=models.CharField(max_length=20)

    date_joined         =models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login          =models.DateTimeField(verbose_name="last login",auto_now_add=True)
    is_active           =models.BooleanField(default=True)
    is_admin            =models.BooleanField(default=False)
    is_staff            =models.BooleanField(default=True) 
    is_superadmin       =models.BooleanField(default=False)
    is_blocked          =models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name','phone_number']

    objects=MyAccountManager()
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True



