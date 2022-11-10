from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from orders.models import Order,OrderItem
from userapp.models import Address
from .forms import CreateUserForm
from django.contrib import messages
from multiprocessing import context
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from account.models import Account
import random
from twilio.rest import Client
from django.views.decorators.cache import never_cache
from twilio.rest import Client
from categories.models import Main_Category,Sub_Category, Product
from cartapp.models import Cart,CartItem
from cartapp.views import _cart_id
from django.db import models
import os
from django.views.decorators.cache import cache_control
from userapp .forms import UserAddressForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# from .models import *
# Create your views here.


def user_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(email=email,password=password)
        
        if user is not None and user.is_blocked is False:
            if user.is_superadmin==False:
                try:
                    
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_item=CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user=user
                            item.save()
                except:
                    pass
                if user.is_superadmin==False:
                    login(request,user)
                    return redirect('home')
                else:
                    return redirect('admin_login')
        else:
            messages.info(request,"Phone Number or Password is Incorrect")
            return redirect(user_login)
    return render(request,'userapp/login.html')
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
    maincategory=Main_Category.objects.all()
    subcategory=Sub_Category.objects.all()
    topitems=Product.objects.all().order_by('created_date')[3::-1]
    cartitem=CartItem.objects.all()
    cart=Cart.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superadmin is False:
            return render(request,'userapp/index.html',{
        'maincategory':maincategory,
        'subcategory':subcategory,
        'topitems':topitems,
        'cartitem':cartitem,
        'cart':cart,
    })
        else:
            return redirect('admin_login')
    return render(request,'userapp/index.html',{
        'maincategory':maincategory,
        'subcategory':subcategory,
        'topitems':topitems,
        'cartitem':cartitem,
        'cart':cart,
    })
# def base(request):
#     maincategory=Main_Category.objects.all()
#     subcategory=Sub_Category.objects.all()
#     products=Product.objects.all()
#     user=Account.objects.all()
#     cart_items=CartItem.objects.all()
#     return render(request,'userapp/base.html',{

#         'user':user,

#     })


def dashboard(request):
    total=0
    tax=0
    orders = Order.objects.filter(user=request.user)
    order_item=OrderItem.objects.all()

    for item in order_item:
        total=total+(item.product.price*item.quantity)
    tax=(50/1000)*total



    print('..............................',orders)
    context={
        'orders':orders,
        'order_item':order_item,
        'tax':tax,
    }
    return render(request,'userapp/dashboard.html',context)





@login_required(login_url='user_login')    
def user_logout(request):
    logout(request)
    response=redirect('user_login')
    return response
@never_cache
def otp_login_page(request):
    return render(request,'userapp/otp_login_page.html')
@never_cache
def otp_login(request):
        if request.method =='GET':
            phone_number=request.GET.get('phone_number')
            print(phone_number)
            user=Account.objects.filter(phone_number=phone_number)
            if not user.exists():
                messages.error(request,"please enter A valid mobile number")
                return redirect(otp_login_page)
            else:
                print('snedinging otp...................................')
                OtpGenerate.send_otp(phone_number)
                return redirect('enter_otp')

def enter_otp(request):   #modification necessary
    main_category=Main_Category.objects.all()
    sub_category=Sub_Category.objects.all()
    products=Product.objects.all()
    context={
    'main_category':main_category,
    'sub_category':sub_category,
    'products':products,
    }
    if request.user.is_authenticated:
        if request.user.is_superadmin is False:
            return render(request,'userapp/index.html',context)
        else:
            return redirect('home')    
    return render(request,'userapp/enter_otp.html')
@never_cache
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
        auth_token='309ac70b4b050464550b95e61004da4d'
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



def view_address(request):
    address=Address.objects.filter(user=request.user)

    return render(request,'userapp/address.html',{
        'address':address
    })


@login_required(login_url='user_login')
def add_address(request):
    address_form=UserAddressForm()
    if request.method=='POST':
        address_form=UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form=address_form.save(commit=False)
            address_form.user=request.user
            address_form.save()
            # messages.success(request, "Successfully new address added")
            return HttpResponseRedirect(reverse('view_address'))
        else:
            address_form=UserAddressForm()

    return render(request,'userapp/add_address.html',{
        'form':address_form,
    })



# .....................shopppppppp................








