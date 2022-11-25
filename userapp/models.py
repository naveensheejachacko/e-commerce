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



class UserProfile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to="userprofile")
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"
