import random
from django.contrib import messages
from django.shortcuts import render
from orders.models import Order, OrderItem
from cartapp.models import CartItem
from categories.models import Product
from userapp.models import Address
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.





@login_required(login_url='user_login')
def place_order(request):
    if request.method=='POST':
        neworder=Order()
        neworder.user=request.user
        neworder.address=Address.objects.get(id=request.POST.get('radio-address'))
        neworder.payment_mode=request.POST.get('payment_mode')
        
        cart_items=CartItem.objects.filter(user=request.user)
        cart_total_price=0
        tax=0

        for cart_item in cart_items:
            tax=(5*cart_item.product.price)/100
            cart_total_price+=((cart_item.product.price+tax)*cart_item.quantity)
        neworder.total_price=cart_total_price
        trackno=str(random.randint(11111,99999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno=str(random.randint(11111,99999))

        neworder.tracking_no=trackno
        neworder.save()
         
        neworderitems =CartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,

            )
      
            print('hello')
            #item reduce
            orderproduct=Product.objects.filter(id=item.product_id).first()
            orderproduct.stock-=item.quantity
            orderproduct.save()



        CartItem.objects.filter(user=request.user).delete()
        messages.success(request,'Your order has been succesfully Placed')
    return redirect('dashboard')


        






# def summary(request):
#     orders=Order.objects.filter(user=request.user)
#     orderitem=OrderItem.objects.filter(user=request.user)
#     print(orders,'..................................')

#     context={
#         'orders':orders,
#         'orderitem':orderitem,
#     }
#     return render(request,'userapp/dashboard.html',context)