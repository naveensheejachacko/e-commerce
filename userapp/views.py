from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from account.models import Account
import random
from twilio.rest import Client


# from .models import *
# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        print("show home page")
        return redirect('home')
    else:
        if request.method=='POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            user=authenticate(email=email,password=password)
            if user is not None :
                if user.is_admin is False:
                    if user.is_blocked:
                        messages.error(request, 'You are restricted by admin')
                        return redirect('user_login')
                    print("SHow homepage if not superadmin")
                    login(request,user)
                    return redirect('home')
                else:
                    print("show admin login")
                    return redirect('admin_login')
                    

            else:
                messages.info(request,'email Or Password is Incorrect!')
                print("incorrect")
                # return render(request,'userapp/sample.html')
                return redirect('user_login')
        return render(request,'userapp/login.html',)
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form=CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                #user=form.cleaned_data.get('username')
                #messages.success(request,'Account was created for' +user)
                return redirect('user_login')
    context={'form':form}
    return render(request,'userapp/signup.html',context)

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superadmin is False:
            return render(request,'userapp/index.html')
        else:
            return redirect('admin_login')
    return render(request,'userapp/index.html')
@login_required(login_url='user_login')    
def user_logout(request):
    logout(request)
    response=redirect('user_login')
    return response

def otp_login_page(request):
    return render(request,'userapp/otp_login_page.html')

def otp_login(request):
        if request.method =='GET':
            phone_number=request.GET.get('phone_number')
            print(phone_number)
            OtpGenerate.send_otp(phone_number)
            return redirect('enter_otp')

def enter_otp(request):
    return render(request,'userapp/enter_otp.html')

def verify_otp(request):
    obj=OtpGenerate()
    if request.method=='POST':
        re_otp=request.POST.get('otp')
        ge_otp=obj.Otp
        if re_otp==ge_otp:
            user=Account.objects.get(phone_number=obj.phone_number)
            if request.user.is_superuser is False:
                login(request,user)
                return redirect('home')
        else:
            messages.error(request,"Invalid Otp")
            return redirect('enter_otp')
    else:
        messages.error(request,"Invalid Credentials")
        return redirect('otp_login_page')

class OtpGenerate():
    Otp=None
    phone=None

    def send_otp(phone_number):
        account_sid='AC53df4905dd72be8bff81dcd8e360d062'
        auth_token='3fa70f103df0683fe792c49ad4500958'
        target_number = '+91' + phone_number
        twilio_number='+15095161694'
        otp=random.randint(1000,9999)
        OtpGenerate.Otp=str(otp)
        OtpGenerate.phone_number=phone_number
        msg="your otp is " + str(otp)
        client=Client(account_sid,auth_token)
        message=client.messages.create(
        body=msg,
        from_=twilio_number,
        to=target_number
        )
        print(message.body)
        return True
