
import datetime
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from offer.models import Coupon
from orders.models import Order,OrderItem
from store.models import Banners
from userapp.models import Address, UserProfile
from .forms import CreateUserForm, UserForm, UserProfileForm
from django.contrib import messages
from multiprocessing import context
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from account.models import Account
import random
from twilio.rest import Client
from django.views.decorators.cache import never_cache
from twilio.rest import Client
from categories.models import Main_Category,Sub_Category, Product, Variations
from cartapp.models import Cart,CartItem
from cartapp.views import _cart_id
from django.db import models
import os
from django.views.decorators.cache import cache_control
from userapp .forms import UserAddressForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib import auth
from decouple import config

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
                            product_variation = []
                        for item in cart_item:
                            variation=item.variations.all()
                            product_variation.append(list(variation))
                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variations = item.variations.all()
                            ex_var_list.append(list(existing_variations))
                            id.append(item.id)


                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity = item.quantity + 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
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
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                phone_number = request.POST['phone_number']
                password = request.POST['password1']
                username = request.POST['username']
                request.session["first_name"]=first_name
                request.session["last_name"]=last_name
                request.session["email"]=email
                request.session["phone"]=phone_number
                request.session["password"]=password
                request.session["username"]=username
                OtpGenerate.send_otp(phone_number)
                return redirect('signup-otp')

    return render(request,'userapp/signup.html',{
        'form':form
    })

            

def signup_otp(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'userapp/signup-otp.html')
def verify_signup_otp(request):
    obj=OtpGenerate()
    if request.method=='POST':
        re_otp=request.POST.get('otp')
        ge_otp=obj.Otp
        if re_otp==ge_otp:
            username=request.session["username"]
            first_name=request.session["first_name"]
            last_name=request.session["last_name"]
            email=request.session["email"]
            phone_number=request.session["phone"]
            password=request.session["password"]


            user=Account.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password
            )
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = "avatar.jpeg"
            profile.save()




            user.phone_number=phone_number
            user.save()
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid Otp")
            return redirect('signup-otp')
    else:
        messages.error(request,"Invalid Credentials")
        return redirect('signup-otp')




def home(request):

    maincategory=Main_Category.objects.all()
    subcategory=Sub_Category.objects.all()
    topitems=Product.objects.filter(is_available=True).order_by('created_date') [:4]
    variations = Variations.objects.all()
    cartitem=CartItem.objects.all()
    coupons=Coupon.objects.all()
    banners = Banners.objects.all()
    print('..................................................................',banners)
    cart=Cart.objects.all()
    orders=Order.objects.all()
    orderitems=OrderItem.objects.all()
    tax=0
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)

        # for cart_item in cart_items:
        #     total+=(cart_item.product.price*cart_item.quantity)
        #     quantity+=cart_item.quantity
        # tax=(5*total)/100
        # grand_total=total+tax
        
    except: 
        pass




    if request.user.is_authenticated:
        if request.user.is_superadmin is False:
            return render(request,'userapp/index.html',{
        'maincategory':maincategory,
        'subcategory':subcategory,
        'topitems':topitems,
        'cartitem':cartitem,
        'cart':cart,
        'orders':orders,
        'orderitems':orderitems,
        'variations': variations,
        'coupons':coupons,
        'banners':banners,
    })
        else:
            return redirect('admin_login')
    return render(request,'userapp/index.html',{
        'maincategory':maincategory,
        'subcategory':subcategory,
        'topitems':topitems,
        'cartitem':cartitem,
        'cart':cart,
        'orderitems':orderitems,
        'variations': variations,
        'coupons':coupons,
        'banners':banners,
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

@login_required(login_url="user_login")
def  dashboard(request):
    orders = OrderItem.objects.filter(
        user=request.user,status="Delivered"
    ).order_by("-created_at") 



    order = Order.objects.order_by("-created_at").filter(
        user_id=request.user.id
    )

    print('.......................................................userprofile 1',orders,'...................................')
    orders_count = order.count()
    print('...............................',orders_count,'.............................')

    userprofile = UserProfile.objects.filter(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
        'orders':orders,

    }

    return render(request, 'userapp/dashboard.html', context)





@login_required(login_url="user_login")
def edit_profile(request):
    print('................hi.......................')
    userprofile =get_object_or_404(UserProfile,user=request.user)
    print('...............................',userprofile,'..........................')
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "userprofile": userprofile,
    }
    return render(request,'userapp/editprofile.html', context)


@login_required(login_url="user_login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, "Password Updated Successfully.")
                return redirect("change_password")
            else:
                messages.error(request, "Your Existing Password Is Incorrect")
                return redirect("change_password")
        else:
            messages.info(request, "Password Does Not Match!")
            return redirect("change_password")

    return render(request, "userapp/change_password.html")
@login_required(login_url="user_login")
def order_summary(request):
    orders=Order.objects.filter(user=request.user).order_by('created_at')[::-1]
    paginator=Paginator(orders,8)
    page=request.GET.get('page')
    paged_orders=paginator.get_page(page)
    return render(request,'userapp/ordersummary.html',{
        
        'orders':paged_orders,
    })

@login_required(login_url="user_login")
def orderview(request,id):
    orders=Order.objects.filter(id=id).filter(user=request.user).first()
    order_items=OrderItem.objects.filter(order=orders)
    context={
        'orders':orders,
        'order_items':order_items
    }
    return render(request,'userapp/orderview.html',context)

@login_required(login_url="user_login")
def user_orders(request):
    orders = OrderItem.objects.filter(
    user=request.user
    ).order_by("-created_at")



    order = Order.objects.order_by("-created_at").filter(
        user_id=request.user.id
    )

    print('.......................................................userprofile 1',orders,'...................................')
    orders_count = order.count()
    print('...............................',orders_count,'.............................')

    userprofile = UserProfile.objects.filter(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
        'orders':orders,

    }

    return render(request, 'userapp/user_orders.html', context)



@login_required(login_url="user_login")
def cancel_order(request, pk):
    product = OrderItem.objects.get(pk=pk)
    product.status = "Cancelled_item"
    product.save()
    item = Product.objects.get(pk=product.product.id)
    item.stock += product.quantity
    item.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def return_order(request,id):
    order_item=OrderItem.objects.get(id=id)
    order_item.status="return"
    order_item.save()
    
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def accept_return(request,id):
    
    order_item=OrderItem.objects.get(id=id)
    
    order_item.status="Refund Initiated"
    product_id=order_item.product_id
    product=Product.objects.get(id=product_id)
    product.stock+=order_item.quantity
    order_item.save()
    product.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])






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
            if user.is_blocked == False :
                try:
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_item=CartItem.objects.filter(cart=cart)
                        product_variation = []
                        for item in cart_item:
                            variation=item.variations.all()
                            product_variation.append(list(variation))
                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variations = item.variations.all()
                            ex_var_list.append(list(existing_variations))
                            id.append(item.id)


                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity = item.quantity + 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass

            if user.is_superadmin == False:
                login(request,user)
                return redirect('home')
        else:
            messages.error(request,"Invalid Otp")
            return redirect('enter_otp')
    else:
        messages.error(request,"Invalid Credentials")
        return redirect('enter_otp')



class OtpGenerate():
    Otp=None
    phone=None

    def send_otp(phone_number):
        account_sid=config('account_sid')
        auth_token=config('auth_token')
        target_number = '+918111850031'
        twilio_number=config('twilio_number')
        otp=random.randint(1000,9999)
        OtpGenerate.Otp=str(otp)
        OtpGenerate.phone_number=phone_number
        msg="your otp for login to Electromart is " + str(otp)
        client=Client(account_sid,auth_token)
        message=client.messages.create(
        body=msg,
        from_=twilio_number,
        to=target_number
        )
        print(message.body)
        return True


@login_required(login_url="user_login")
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

@login_required
def delete_address(request, pk):
    dlt = Address.objects.filter(id=pk)
    print(dlt)
    dlt.delete()
    messages.success(request, "Your Address Has been deleted")
    return redirect("view_address")





# def ordersummary(request,id):
#         # try:
#     orders=Order.objects.get(id=id,user=request.user)
      
#         # except:
#         #     return HttpResponse("not found")
#     data={
#             'order_id':orders.id,
#             'date':str(orders.created_at),
#             'name':orders.user.first_name,
#             'address':orders.address.address,
#             'total_price':orders.total_price,
#             'payment_id':orders.payment_id,
#             'payment_mode':orders.payment_mode,
#             'user_email':orders.user.email,
#             'orders':orders,
#         }
#     return render(request,'userapp/ordersummary.html',data)




from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.views.generic import View
from django.template.loader import get_template
class generateInvoice(View):

    def get(self,request,id,*args,**kwargs):
        try:
            orders=Order.objects.get(id=id,user=request.user)
            print(orders,'..............')
            # orderitem=OrderItem.objects.get(id=id,user=request.user)
            # print(orderitem)
            # print('............................')
            date=orders.created_at.strftime("%A,%d-%m-%Y")
            
        except:
            print('invoice cant print')
            return HttpResponse("505 not found")
        data={
            'order_id':orders.id,
            'date':date,
            'name':orders.user.first_name,
            'address':orders.address.address,
            'total_price':orders.total_price,
            'transaction_id':orders.payment_id,
            'payment_mode':orders.payment_mode,
            'user_email':orders.user.email,
            'orders':orders,
        }
        pdf=render_to_pdf('userapp/invoice.html',data)
        return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

# .....................shopppppppp................

#widhlist
@login_required(login_url="user_login")
def user_wishlist(request):
    products=Product.objects.filter(users_wishlist=request.user)
    
    return render(request,'userapp/wishlist.html',{
        'wishlist':products,
    })


def add_to_wishlist(request,id):
    product=get_object_or_404(Product,id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
       
    else:
        product.users_wishlist.add(request.user)
        
    return HttpResponseRedirect(request.META["HTTP_REFERER"])






