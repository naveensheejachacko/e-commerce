from django.db import models
from account.models import Account
# Create your models here.
class Address(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    fname=models.CharField(max_length=150,null=False)
    lname=models.CharField(max_length=150,null=False)
    email=models.CharField(max_length=150,null=False)
    phone_number=models.CharField(max_length=20)
    address=models.CharField(max_length=150,null=False)
    country=models.CharField(max_length=150,null=False)
    state=models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=150,null=False)
    # default=models.BooleanField("default",default=False)

class Sample(models.Model):
    fname=models.CharField(max_length=150,null=False)