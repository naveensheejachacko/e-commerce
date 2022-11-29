
from django.shortcuts import get_object_or_404, render, redirect
from categories.models import Main_Category,Sub_Category, Product, Variation
from offer.models import Coupon,ReviewCoupon

from userapp.models import Address
from  .models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from math import prod
from django.http import HttpResponseRedirect, JsonResponse
from datetime import date

# Create your views here.




def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):

    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product

    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                print("................",key,value,"...............................")

                try:
                    print("navvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    product_variation.append(variation)
                except:
                    print("***********except**************")
                    pass
        else:
            print("****else****")
        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    # if the user is not authenticated
    else:

        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(
                cart_id=_cart_id(request)
            )  # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart
        ).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print("..................",ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')



def remove_cart(request,product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id
            )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


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
    tax=0
    grand_total=0
    total_price=0
    saved=0
    maincategory=Main_Category.objects.all()
    subcategory=Sub_Category.objects.all()
    variations=Variation.objects.all()
    try:
        if "product_id" in request.session:
            del request.session["product_id"]
        
        else:
            if request.user.is_authenticated:
                cart_items=CartItem.objects.filter(user=request.user,is_active=True)
            else:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                cart_items=CartItem.objects.filter(cart=cart,is_active=True)

            for cart_item in cart_items:
                if cart_item.product.offer_price():
                        total_price+=(cart_item.product.price*cart_item.quantity)
                        offer_price=Product.offer_price(cart_item.product)
                        total+=(offer_price["new_price"]*cart_item.quantity)
                else:
                    total_price+=(cart_item.product.price*cart_item.quantity)
                quantity+=cart_item.quantity
                saved=total_price-total

            grand_total=total
    except ObjectDoesNotExist: 
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,

        'grand_total':grand_total,
        'maincategory':maincategory,
        'subcategory':subcategory,
        "variations":variations,
        'saved': saved,
        'total_price':total_price,
    }
    return render(request,'cartapp/cart.html',context)

@login_required(login_url='user_login')
def checkout(request,total=0,quantity=0):
    address=Address.objects.filter(user=request.user)

    grand_total=0
    without_offer=0
    # cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        if cart_item.product.offer_price():
                without_offer+=(cart_item.product.price*cart_item.quantity)
                offer_price=Product.offer_price(cart_item.product)
                total+=(offer_price["new_price"]*cart_item.quantity)
        else:
            total+=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
        

    grand_total=total
    usd=int(grand_total/82)

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    
        'grand_total':grand_total,
        'address':address,
        'usd':usd,
        'without_offer':without_offer,
     
    }
    return render(request,'cartapp/checkout.html',context)



def apply_coupon(request):
    print('hiiiiiiiiiiiiiiiiiiiii')
   
    grand_total=0
    total=0
    cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        print('.................forloop............')
        if cart_item.product.offer_price():
            offer_price=Product.offer_price(cart_item.product)
            total+=(offer_price["new_price"]*cart_item.quantity)
        else:
            total+=(cart_item.product.price*cart_item.quantity)
    if request.method=='GET':
        print('...............if 1....................')
        code=request.GET.get('code')
        print('.....................',code,'.............................')
        coupon=Coupon.objects.get(code=code)
        today=date.today()
        if coupon.valid_from <= today and coupon.valid_to >= today:
            print('.....................if 2.....................')
            total-=coupon.discount
            cart_item.coupon_discount=total
            cart_item.save()  
    return JsonResponse({
        'total':total,
        'discount':coupon.discount,
        'grand_total':grand_total,
    })


