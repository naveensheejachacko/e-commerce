
from django.contrib.auth.forms import UserCreationForm
from django import forms
from  account .models import Account
from django.contrib.auth.forms import (AuthenticationForm)
from .models import Address

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','username','email','phone_number','password1','password2']


class UserAddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=["fname","lname",'address',"country",'pincode','state','email','phone_number']

        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["fname"].widget.attrs.update(
                {"class":"form-control","placeholder":"Full Name"}
            )

            self.fields["lname"].widget.attrs.update(
                {"class":"form-control","placeholder":"Last Name"}
            )

            self.fields["address"].widget.attrs.update(
                {"class":"form-control","placeholder":"Address"}
            )

            self.fields["pincode"].widget.attrs.update(
                {"class":"form-control","placeholder":"Pincode"}
            )

            self.fields["country"].widget.attrs.update(
                {"class":"form-control"}
            )
            self.fields["state"].widget.attrs.update(
                {"class":"form-control"}
            )
            self.fields["email"].widget.attrs.update(
                {"class":"form-control","placeholder":"Email"}
            )
            self.fields["phone_number"].widget.attrs.update(
                {"class":"form-control","placeholder":"Phone Number"}
            )