from django.shortcuts import render,get_object_or_404
from  categories.models import Product,Main_Category,Sub_Category
from cartapp.models import Cart,CartItem
from django.urls import reverse
from cartapp.views import _cart_id
from django.http import HttpResponse
from cartapp.models import CartItem,Cart
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger 
from django.db .models import Q
# Create your views here.


def store(request,maincategory_slug=None,subcategory_slug=None):
    maincategories=None
    subcategories=None
    products=None
    main_category=Main_Category.objects.all()
    sub_category=Sub_Category.objects.all()
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
        'product_count':product_count
    }
    return render(request,'storeapp/store.html',context)

def product_details(request,maincategory_slug,subcategory_slug,product_slug):
    main_category=Main_Category.objects.all()
    sub_category=Sub_Category.objects.all()
    
    try:
        single_product=Product.objects.get(parent_main_prdt__slug=maincategory_slug,parent_sub_prdt__slug=subcategory_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    except Exception as e:
        raise e
    

    return render(request,'storeapp/product_details.html',{
        'main_category':main_category,
        'sub_category':sub_category,
        'single_product':single_product,
        'in_cart':in_cart,
    
    })

def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if 'keyword':
            products=Product.objects.order_by('-created_date').filter(Q(prdt_desc__icontains=keyword)|Q(product_name=keyword))
            product_count=products.count()
    context={
        'products':products,
        'product_count':product_count
    }
    return render(request,'storeapp/store.html',context)
