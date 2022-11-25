from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache

from account.models import Account
from cartapp.models import Cart, CartItem
from categories.models import Product
from orders.models import STATUS1, Order, OrderItem

from django.utils import timezone
from django.db.models import Sum
# import csv
import datetime
# import tempfile
from datetime import date
from django.utils.timezone import localtime, now




from django.db.models import Count,Q


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
        exclude_list = [
        "Cancelled_item",
        "Refund_Initiated",
        ]
        products = Product.objects.all()
        total_users=Account.objects.filter(Q(is_active=True)& Q(is_admin=False)).count()
        day=datetime.datetime.now()
        visitors=Account.objects.filter(last_login=day).count()

        total_revenue = OrderItem.objects.filter(status="Delivered").aggregate(Sum("price"))
        total_orders = OrderItem.objects.all().exclude(status__in=exclude_list).count()
        print('...................',total_orders,'.total orders...........................')
        total_products = Product.objects.filter(is_available=True).count()
        print('............................',visitors,'..visit today...............................')
        # sales/orders
        current_year = timezone.now().year
        order_detail = OrderItem.objects.filter(
            created_at__lt=datetime.date(current_year, 12, 31),
            status="Delivered",
        ) 
        monthly_order_count = []
        month = timezone.now().month
        print(month)
        for i in range(1, month + 1):
            monthly_order = order_detail.filter(created_at__month=i).count()
            monthly_order_count.append(monthly_order)

        # status

        today=datetime.datetime.now()
        dates=OrderItem.objects.filter(created_at__month=today.month).values('created_at__date').annotate(order_items=Count('id',filter=Q(status='Placed'))).order_by('created_at__date')
        returns=OrderItem.objects.filter(created_at__month=today.month).values('created_at__date').annotate(returns=Count('id',filter=(Q(status="Cancelled_item") | Q(status="Refund Initiated")))).order_by('created_at__date')
        sales=OrderItem.objects.filter(created_at__month=today.month).values('created_at__date').annotate(sales=Count('id',filter=Q(status="Delivered"))).order_by('created_at__date')

        # new_count = OrderItem.objects.filter(status="New").count()
        # placed_count = OrderItem.objects.filter(status="Placed").count()
        # shipped_count = OrderItem.objects.filter(status="Shipped").count()
        # accepted_count = OrderItem.objects.filter(
        #     status="Accepted"
        # ).count()
        # delivered_count = OrderItem.objects.filter(
        #     status="Delivered"
        # ).count()
        # cancelled_count = OrderItem.objects.filter(
        #     status="Cancelled_item"
        # ).count()




        # most moving product
        most_moving_product_count = []
        most_moving_product = []
        for i in products:
            most_moving_product.append(i)
            most_moving_product_count.append(
                OrderItem.objects.filter(
                    product=i, status="Delivered"
                ).count()
            )

        print(most_moving_product)
        print(most_moving_product_count)
        placed_count=OrderItem.objects.filter(status="Placed").count()
        shipped_count=OrderItem.objects.filter(status="Shipped").count()
        delivered_count=OrderItem.objects.filter(status="Delivered").count()
        return_count=OrderItem.objects.filter(status="Refund Initiated").count()
        cancelled_count=OrderItem.objects.filter(status="Cancelled_item").count()

        context = {

            "monthly_order_count": monthly_order_count,

            'today':today,
            'sales':sales,
            'returns':returns,
            'dates':dates,


            "most_moving_product_count": most_moving_product_count,
            "most_moving_product": most_moving_product,

            'total_users':total_users,
            'visitors':visitors,
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_products": total_products,
            'status_count':[
                placed_count,
                shipped_count,
                delivered_count,
                return_count,
                cancelled_count,
            ]
        }
        return render(request, "adminapp/admin_home.html", context)
    else:
        return redirect("admin_login")
   
def admin_logout(request):
    print("logout")
    logout(request)
    return redirect('admin_login')

    #prfdt management

def user_manage(request):
    context={'user_details':Account.objects.all().order_by('-id')}#show user details
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





def activeorders(request):
    
    exclude_list = [
        "Delivered",
        "Cancelled_item",
        "Refund Initiated"
    ]
    active_orders =OrderItem.objects.all().exclude(
        status__in=exclude_list
    )#for reversing order
    status=STATUS1
    context ={
        "active_orders":active_orders,
        "status":status,
    }
    return render(request,'adminapp/active_orders.html',context)


def order_history(request):
    exclude_list = [
        "New",
        "Accepted",
        "Placed",
        "Shipped",
    ]
    active_orders = OrderItem.objects.all().exclude(
        status__in=exclude_list
    )[::-1]
    status = STATUS1
    context = {
        "active_orders": active_orders,
        "status": status,
    }
    return render(request, "adminapp/order_history.html", context)


def order_status_change(request):
    id = request.POST['id']
    status = request.POST['status']
    order_item = OrderItem.objects.get(id=id)
    order_item.status = status
    order_item.save()
    return JsonResponse({"success": True})