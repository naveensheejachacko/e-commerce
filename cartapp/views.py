
from django.shortcuts import get_object_or_404, render, redirect
from categories.models import Color, Main_Category, Size,Sub_Category, Product, Variations
from offer.models import Coupon

from userapp.models import Address
from  .models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from math import prod
from django.http import HttpResponseRedirect, JsonResponse
from datetime import date
from django.contrib import messages
# Create your views here.




def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product_variation=[]
    current_user=request.user
    product=Product.objects.get(id=product_id)
    if request.method=="POST" and request.POST.get('color') and request.POST.get('size'):
        c=request.POST.get('color')
        
        s=request.POST.get('size')
        
        
        try:
            variation=Variations.objects.get(product=product,color=c,size=s)
            product_variation.append(variation)
        except:
            pass
    else:
        messages.error(request,'Choose size and colour..!!')
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    if current_user.is_authenticated:
        is_cart_item_exists=CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user=current_user)

            ex_var_list=[]
            id=[]

            for item in cart_item:
                exsisting_varation=item.variations.all()
                ex_var_list.append(list(exsisting_varation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,

            )
            if len(product_variation) >0:
                cart_item.variations.clear()
                
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:

        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)

            ex_var_list=[]
            id=[]

            for item in cart_item:
                exsisting_varation=item.variations.all()
                ex_var_list.append(list(exsisting_varation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,

            )
            if len(product_variation) >0:
                cart_item.variations.clear()
                
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return HttpResponseRedirect(request.META["HTTP_REFERER"])




# def remove_cart(request,product_id,cart_item_id):
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(
#                 product=product, user=request.user, id=cart_item_id
#             )
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(
#                 product=product, cart=cart, id=cart_item_id
#             )
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
#     except:
#         pass
#     return redirect('cart')


def delete_cart_item(request,product_id,cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
            cart_item=CartItem.objects.filter(product=product,user=request.user,id=cart_item_id)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
def cart(request,total=0,quantity=0,cart_items=None):
    category=Main_Category.objects.all()
    total_price=0
    saved=0
    sub_total=0
    subcategory=Sub_Category.objects.all()
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        
        for cart_item in cart_items:
            total_price+=(cart_item.product.price*cart_item.quantity)
            if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                total+=(offer_price["new_price"]*cart_item.quantity)
                total=round(total,2)
            else:
                total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
            sub_total=cart_item.sub_total()
            saved=total_price-total
            saved=round(saved,2)
    except:
        pass
    return render(request,'cartapp/cart.html',{
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'category':category,
        'subcategory':subcategory,
        'total_price':total_price,
        'saved':saved,
        'sub_total':sub_total,
    })


@login_required(login_url='user_login')

def checkout(request,total=0,quantity=0):
    tax=0
    usd=0
    coupons=Coupon.objects.all()
    address=Address.objects.filter(user=request.user)
    cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                total+=(offer_price["new_price"]*cart_item.quantity)
                total=round(total,2)
        else:
            total+=(cart_item.product.price*cart_item.quantity)
        
    
        quantity+=cart_item.quantity
    usd=total/83
    return render(request,'cartapp/checkout.html',{
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'address':address,
        'coupons':coupons,
        'usd':usd,
        'tax':tax,
    })

# coupon apply

def apply_coupon(request):
    tax=0
    total=0
    cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        if cart_item.product.offer_price():
            offer_price=Product.offer_price(cart_item.product)
            total+=(offer_price["new_price"]*cart_item.quantity)
            total=round(total,2)
        else:
            total+=(cart_item.product.price*cart_item.quantity)
    
    if request.method=='GET':
        code=request.GET.get('code')
        coupon=Coupon.objects.get(code=code)
        if Coupon.objects.filter(code=code).exists():
            c_exists=True
            today=date.today()
            if coupon.valid_from <= today and coupon.valid_to >= today:
                total-=coupon.discount
                cart_item.coupon_discount=total
                cart_item.save()
                status=True
            else:
                status=False
        else:
            c_exists=False
            print('coupon not found')
            return redirect('checkout')
    return JsonResponse({
        'total':total,
        'discount':coupon.discount,
        'status':status,
        'c_exists':c_exists,
        'tax':tax,
    })


# ajax





def decrease_quantity(request):
    tax=0
    product_id=request.GET.get('id')
    product=get_object_or_404(Product,id=product_id)
    id_cart=request.GET.get('c_id')

    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(id=id_cart,product=product,user=request.user)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(id=id_cart,product=product,cart=cart)

    if cart_item.quantity: 
        
            
        qty = cart_item.quantity - 1
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            status=False
            cart_item.quantity=1
            cart_item.save()
        else:
            status=True
            cart_item.save()
        
        total_price=(cart_item.product.price*cart_item.quantity)
        total=0
        if cart_item.product.offer_price():
            offer_price=Product.offer_price(cart_item.product)
            total+=(offer_price["new_price"]*cart_item.quantity)
            total=round(total,2)
        else:
            total+=(cart_item.product.price*cart_item.quantity)
        cart_item.offer_discount=total
        cart_item.save()
        sub_total=cart_item.sub_total()
        you_saved=total_price-total
        saved=round(you_saved,2)


        
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        total_p=0
        total_price_p=0
        for cart_item in cart_items:
            total_price_p+=(cart_item.product.price*cart_item.quantity)
            if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                total_p+=(offer_price["new_price"]*cart_item.quantity)    
                total_p=round(total_p,2)
            else:
                total_p+=(cart_item.product.price*cart_item.quantity)
            
            saved_p=total_price_p-total_p
            saved_p=round(saved_p,2)
    print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
    return JsonResponse({
        'quantity':qty,
        'total':total_p,
        'sub_total':sub_total,
        'total_price':total_price_p,
        'saved':saved_p,
        'status':status,
        'tax':tax,
        
        

    })


def increase_quantity(request):
    tax=0
    product_id=request.GET.get('id')
    id_cart=request.GET.get('c_id')
    print('#########################',id_cart)
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(id=id_cart,product=product,user=request.user)
        print('................if1....................')
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(id=id_cart,product=product,cart=cart)
    if cart_item.quantity:
        qty = cart_item.quantity + 1
        cart_item.quantity += 1
        cart_item.save()
        total_price=(cart_item.product.price*cart_item.quantity)
        total=0
        print('................if2....................')
        if cart_item.product.offer_price():
            offer_price=Product.offer_price(cart_item.product)
            total+=(offer_price["new_price"]*cart_item.quantity)
            total=round(total,2)
        else:
            total+=(cart_item.product.price*cart_item.quantity)
        cart_item.offer_discount=total
        cart_item.save()
        sub_total=cart_item.sub_total()
        you_saved=total_price-total
        saved=round(you_saved,2)
        
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        total_p=0
        total_price_p=0
        for cart_item in cart_items:
            total_price_p+=(cart_item.product.price*cart_item.quantity)
            if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                total_p+=(offer_price["new_price"]*cart_item.quantity)    
                total_p=round(total_p,2)
            else:
                total_p+=(cart_item.product.price*cart_item.quantity)
            
            saved_p=total_price_p-total_p
            saved_p=round(saved_p,2)
    
    return JsonResponse({
        'quantity':qty,
        'total':total_p,
        'sub_total':sub_total,
        'total_price':total_price_p,
        'saved':saved_p,
        'tax':tax,   

    })