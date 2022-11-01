from django import forms

from django.contrib.auth.forms import UserCreationForm
from django import forms
from  account .models import Account

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','username','email','phone_number','password1','password2']