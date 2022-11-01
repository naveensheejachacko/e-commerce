from django.views.decorators.cache import never_cache
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from account.models import Account


# Create your views here.
def admin_login(request):
    if request.user.is_authenticated:
        print("home admin")
        return redirect('admin_home')
    if request.method=='POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                if user.is_admin:
                    login(request,user)
                    print("admin home after auth")
                    return redirect('admin_home')
                    
                else:
                    print("redirect admin login")
                    return redirect('admin_login')
            else:
                messages.info(request,'username Or Password is Incorrect!') 
                print("error")
                return redirect('admin_login')
                
    return render(request,'adminapp/admin_login.html')
@login_required(login_url='admin_login')
def admin_home(request):
    if request.user.is_admin:
        return render(request,'adminapp/admin_home.html')#show list
        # context={'user_details':Account.objects.all()}#show user details
    else:
        return redirect('admin_login')
def admin_logout(request):
    print("logout")
    logout(request)
    return redirect('admin_login')

    #prfdt management

def user_manage(request):
    context={'user_details':Account.objects.all()}#show user details
    return render(request,'adminapp/user_manage.html',context)

@login_required(login_url='admin_login')
@never_cache
def block_user(request,bid):
    user =Account.objects.get(id=bid)
    if user.is_blocked:
        print(bid)
        user.is_blocked = False
        user.save()
        return redirect('user_manage')
    else:
        user.is_blocked = True
        user.save()
    print('user blocked')
    return redirect('user_manage')