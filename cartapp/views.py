
from django.shortcuts import get_object_or_404, render, redirect
from categories.models import Main_Category,Sub_Category, Product
from userapp.models import Address
from  .models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from math import prod
from django.http import HttpResponseRedirect

# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id) 
    print(product_id)
    current_user=request.user
    if current_user.is_authenticated:
        try:
            print('......user authenticated try .......')
            cart_item=CartItem.objects.get(product=product,user=current_user)
            cart_item.quantity += 1 
            cart_item.save()
        except CartItem.DoesNotExist:
            print('.............user authenticated except....................')
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
        cart_item.save()
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


    else:

        try:
            print('..................else try block...............')
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            print('........else except block................')
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        try:
            print('..............adding item to cart if exist.............')
            cart_item=CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity+=1
            cart_item.save()
        except CartItem.DoesNotExist:
            print('........addding item if no item in cart............')
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,

            )
        cart_item.save()

    # return redirect('cart')
        return HttpResponseRedirect(request.META["HTTP_REFERER"])



def remove_cart(request,product_id):
    current_user=request.user
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    print('...................',product,'.........................')
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=current_user)
        else:
            cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def delete_cart_item(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
            cart_item=CartItem.objects.filter(product=product,user=request.user)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):
    maincategory=Main_Category.objects.all()
    subcategory=Sub_Category.objects.all()
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)

        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(5*total)/100
        grand_total=total+tax
    except: 
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'maincategory':maincategory,
        'subcategory':subcategory,
    }
    return render(request,'cartapp/cart.html',context)

@login_required(login_url='user_login')
def checkout(request,total=0,quantity=0):
    address=Address.objects.filter(user=request.user)

    tax=0
    grand_total=0
    # cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        total +=(cart_item.product.price*cart_item.quantity)
        quantity +=cart_item.quantity
    tax=(5*total)/100
    grand_total=total+tax

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'address':address,
    }
    return render(request,'cartapp/checkout.html',context)




