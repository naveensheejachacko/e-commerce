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
from django.http import HttpResponse, JsonResponse
# Create your views here.





@login_required(login_url='user_login')
def place_order(request):
    tax=0
    if request.method=='POST':
        neworder=Order()
        neworder.user=request.user
        address=Address.objects.get(id=request.POST.get('address'))
        neworder.address=address
        print(neworder.address)
        neworder.payment_mode=request.POST.get('payment_mode')
        neworder.payment_id=request.POST.get('payment_id')

        
        cart_items=CartItem.objects.filter(user=request.user)
        cart_total_price=0
        trackno=str(random.randint(11111,99999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno=str(random.randint(11111,99999))
        for cart_item in cart_items:
            if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                cart_total_price+=(offer_price["new_price"]*cart_item.quantity)
            else:
                cart_total_price+=(cart_item.product.price*cart_item.quantity)

            if cart_item.coupon_discount:
                cart_total_price=cart_item.coupon_discount
            else:
                pass
        
        neworder.total_price=cart_total_price
        neworder.tax=tax
        neworder.tracking_no=trackno
        neworder.save()
        neworderitems=CartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                user=item.user,
           
                
            )



            orderproduct=Product.objects.filter(id=item.product_id).first()
            orderproduct.stock-=item.quantity
            orderproduct.save()

        
        
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request,'Your order has been placed Succesfully')
        

        pay_mode=request.POST.get('payment_mode')
        if(pay_mode=="Razorpay" or pay_mode=="Paypal"):
            return JsonResponse({'status':"Your order has been placed Succesfully"})

    

    return redirect('dashboard')

def proceed_to_pay(request):
    tax=0
    usd=0
    cart_items=CartItem.objects.filter(user=request.user)
    cart_total_price=0
    for cart_item in cart_items:
        if cart_item.product.offer_price():
            offer_price=Product.offer_price(cart_item.product)
            cart_total_price+=(offer_price["new_price"]*cart_item.quantity)
        else:
            cart_total_price+=(cart_item.product.price*cart_item.quantity)

        if cart_item.coupon_discount:
            cart_total_price=cart_item.coupon_discount
        else:
            pass
    return JsonResponse({
        'total_price':cart_total_price,
        'tax':tax,
                
        
    })




# def cod(request):
#     pass

# @login_required(login_url='user_login')
# def Razorpay(request):
#     cartitem=CartItem.objects.filter(user=request.user)
#     total_price=0
#     tax=0
#     for item in cartitem:
#         sub_total=sub_total+(item.product.price*item.quantity )
#         tax=sub_total*(5/100)
#         total_price=total_price+tax+sub_total
#     return JsonResponse({
#         'total_price':total_price
#     })

# def summary(request):
#     return HttpResponse('succwssss')        





