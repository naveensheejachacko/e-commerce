from django.shortcuts import render,get_object_or_404
from  categories.models import Color, Product,Main_Category,Sub_Category, Variations,Size
from cartapp.models import Cart,CartItem
from django.urls import reverse
from cartapp.views import _cart_id
from django.http import HttpResponse
from cartapp.models import CartItem,Cart
from orders.models import Order,OrderItem
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger 
from django.db .models import Q

# Create your views here.


def store(request,maincategory_slug=None,subcategory_slug=None):
    maincategories=None
    subcategories=None
    products=None
    
    main_category=Main_Category.objects.all()
    sub_category=Sub_Category.objects.all()
    topitems=Product.objects.all()
    # cartitem=CartItem.objects.filter(user=request.user,is_active=True)
    
    cart=Cart.objects.all()
    orders=Order.objects.all()
    orderitems=OrderItem.objects.all()
    if maincategory_slug !=None:
        print('main slug:',maincategory_slug)
        maincategories=get_object_or_404(Main_Category,slug=maincategory_slug)
        products=Product.objects.filter(parent_main_prdt=maincategories,is_available=True)
        paginator=Paginator(products,6 )
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
        if subcategory_slug != None:
            subcategories=get_object_or_404(Sub_Category,slug=subcategory_slug)
            print('sub slug:',subcategory_slug)
            products=Product.objects.filter(parent_sub_prdt=subcategories,is_available=True)
            paginator=Paginator(products,3 )
            page=request.GET.get('page')
            paged_products=paginator.get_page(page)
            product_count=products.count()

    else: 
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,3 )
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    context = {
        'main_category':main_category,
        'sub_category':sub_category,
        'products':paged_products,
        'product_count':product_count,
        # 'cartitem':cartitem,
        'cart':cart,
        'orders':orders,
        'orderitems':orderitems,
        'topitems':topitems,

    }
    return render(request,'storeapp/store.html',context)

def product_details(request,maincategory_slug,subcategory_slug,product_slug):
 
    main_category=Main_Category.objects.all()
    print(".....................entered product details..................")
    
    try:
        product=request.GET.get('product_id')
        single_product=Product.objects.get(parent_main_prdt__slug=maincategory_slug,parent_sub_prdt__slug=subcategory_slug,slug=product_slug)

        #variation=Variations.objects.values('color_id').distinct()
        variation = Variations.objects.filter(product_id=single_product).distinct('color')
        print(variation)
        # for v in variation:
        #     print(v['color'])

            

        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()


        
    except Exception as e:
        print('..................enter exception...................')
        raise e
    

    return render(request,'storeapp/product_details.html',{
        'main_category':main_category,
        'single_product':single_product,
        'in_cart':in_cart,
        'variation':variation,
    
    
    })


def load_size_user(request):

    color=request.GET.get('color_id')
    print(color)
    colorname=Color.objects.get(id=color)
    print('..........................................................',colorname,'***************************')
    size=Size.objects.filter(color_id=colorname.id)

    print('.........................',size)
    
    return render(request,'storeapp/user_size_dropdown.html',{'size':size})


def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if 'keyword':
            products=Product.objects.order_by('-created_date').filter(Q(prdt_desc__icontains=keyword)|Q(product_name__icontains=keyword))
            product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
    }
    return render(request,'storeapp/store.html',context)

def filter_price(request):
    category=Main_Category.objects.all()
    selected=request.GET.get('gridRadios')
    if int(selected) == 1:
        products=Product.objects.filter(Q(price__lte = 100 ))
    elif int(selected) == 2:
        products=Product.objects.filter(Q(price__gte = 100,price__lte=500 ))
    elif int(selected) == 3:
        products=Product.objects.filter(Q(price__gte = 500,price__lte=1000 ))
    elif int(selected) == 4:
        products=Product.objects.filter(Q(price__gte = 1000,price__lte=5000 ))
    elif int(selected) == 5:
        products=Product.objects.filter(Q(price__gte = 5000,price__lte=10000 ))
    else:
        products=Product.objects.filter(Q(price__gte = 10000  ))


    return render(request,'storeapp/filter_store.html',{
        'products':products,
        'category':category
    })
