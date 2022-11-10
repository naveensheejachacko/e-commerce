from ast import Sub
from ast import excepthandler
from multiprocessing import context
from pkgutil import get_data
from django import http
from django.contrib import messages
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from categories.models import Main_Category,Sub_Category, Product
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin_login')
def main_category(request):
    main_category=Main_Category.objects.all().order_by('-id')
    context={
        'main_category':main_category
    }
    return render(request,'adminapp/main_category.html',context)
@login_required(login_url='admin_login')
def main_cat_add_page(request):
    return render(request,'adminapp/addmaincat.html')
@login_required(login_url='admin_login')
def add_main_cat(request):
    if request.POST:
        if request.POST['maincatname'] and request.FILES['maincatimage']:
            print('first iff.......................')
            main_cat_name=request.POST['maincatname']
            main=Main_Category()
            if Main_Category.objects.filter(main_category_name=main_cat_name).exists():
                print('second iff.................................')
                messages.error(request,'Main Category already exists')
                return redirect('add_main_cat')  
            main.main_category_name=main_cat_name
            main.slug = slugify(main_cat_name)
            main.thumbnail=request.FILES['maincatimage']
            main.save()
            messages.error(request, main_cat_name +' category added', extra_tags='added')
            return redirect('main_category')
        else:
            print('3rd if .....................................')
            messages.error(request, 'you cannot submit without credentials filled !', extra_tags='added.')
            return redirect('main_category')
    print('4th')
    return redirect('main_cat_add_page')
@login_required(login_url='admin_login')
def edit_main_cat(request,id):
    main=Main_Category.objects.get(pk=id)
    if request.method=='POST':
        main_cat_name=request.POST.get('maincatname')
        main.main_category_name=main_cat_name
        main.slug=slugify(main_cat_name)
        main.save()
        messages.error(request,"Updated")
        return redirect('main_category')
    return render(request,'adminapp/editmaincat.html',
    {
        'main':main
    })
    

# def main_cat_up(request):
#     if request.POST:
#         main=Main_Category.objects.get(pk=id)
#         main.main_category_name=request.POST['maincatname']
#         main.slug=slugify()
#         main.thumbnail=request.FILES['maincatimage']
#         messages.error(request,'Main Category Updated')
#         return redirect('main_category')

def main_cat_delete(request,id):
    main=Main_Category.objects.filter(id=id).delete()
    return redirect('main_category')

    
    

@login_required(login_url='admin_login')
def subcat_add_page(request):
    main_category=Main_Category.objects.all()
    context={
        'main_category':main_category
    }
    return render(request,'adminapp/add-sub-category.html',context)
@login_required(login_url='admin_login')
def sub_category(request):
    sub_cat=Sub_Category.objects.all().order_by('-id')
    context={
            'sub_cat':sub_cat
        }
    return render(request,'adminapp/sub-category.html',context)


    

# ...............function for category add..............

@login_required(login_url='admin_login')
def subcat_add(request): 
    main=Main_Category.objects.all()
    if request.method=="POST":
        main=request.POST.get('selectmain')
        print(main)
        sub_name=request.POST.get('subcatname')
        print(sub_name)
        if Sub_Category.objects.filter(sub_cat_name=sub_name).exists():
            messages.error(request,' Sub Category Already Exists')
            return redirect(subcat_add)
        else:
            obj=Sub_Category()
            obj.sub_cat_name=sub_name
            obj.slug=slugify(sub_name)
            obj.parent_main_id=main
            obj.save()
            messages.error(request,'SubCategory Created')
            return redirect('sub_category')
    return redirect(subcat_add_page)

@login_required(login_url='admin_login')
def sub_cat_edit_page(request):
    main_category=Main_Category.objects.all()
    context={
        'main_category':main_category
    }
    return render(request,'adminapp/sub_cat_edit.html',context)

@login_required(login_url='admin_login')
def sub_cat_edit(request,id):
    main_category=Main_Category.objects.all()
    if request.method=='POST':
        sub_cat=Sub_Category.objects.get(pk=id)
        main=request.POST.get('selectmain')
        sub_name=request.POST.get('subcatname')
        if Sub_Category.objects.filter(sub_cat_name=sub_name).exists():
            print("exist cond working...........................")
            messages.error(request,'Already Exists')
            return redirect('sub_category')
        else:
            sub_cat.sub_cat_name=sub_name
            sub_cat.slug=slugify(sub_name)
            sub_cat.parent_main_id=main
            sub_cat.save()
            print('updation work......................')
            messages.error(request,'SubCategory Updated')
            return redirect('sub_category')
    print('page showing................................')
    # return redirect('sub_cat_edit_page')
    return render(request,'adminapp/sub_cat_edit.html',{
         'main_category':main_category
    })

def sub_cat_delete(request,id):
    sub=Sub_Category.objects.filter(id=id).delete()
    return redirect('sub_category')

def load_subcategory(request,mid):
    sub_cat=Sub_Category.objects.filter(parent_main_id=mid)
    print(sub_cat,'..............................')
    context={
        'sub_cat':sub_cat
    }
    return render(request,'adminapp/dropdown.html',context)



def dropdown_P(request):
    category = request.GET.get("category")
    
    subcat = Sub_Category.objects.filter(parent_main_id=category).all()
    
    return render(request, "adminapp/dropdown.html",{"subcat":subcat})


#................ products..................
@login_required(login_url='admin_login')
def product(request):
    products=Product.objects.all().order_by('-id')
    return render(request,'adminapp/products.html',{
        'products':products
    })

def add_product_page(request):
    main=Main_Category.objects.all()
    sub_cat=Sub_Category.objects.all()
    context={
        'main':main,
        'sub_cat':sub_cat,
    }
    return render(request,'adminapp/add_products.html',context)
@login_required(login_url='admin_login')
def add_product(request):
    if request.method=="POST":
        productname=request.POST.get('productname')
        if Product.objects.filter(product_name=productname).exists():
            print('...............exist......................')
            messages.error(request,'Product Name Already Exists !')
            return redirect('add_product')
        obj=Product()
        obj.product_name=productname
        obj.slug=slugify(productname)
        obj.prdt_desc=request.POST.get('product_desc')
        obj.price=request.POST.get('price')
        obj.stock=request.POST.get('stock')
        obj.parent_sub_prdt_id=request.POST.get('selectsub')
        obj.parent_main_prdt_id=request.POST.get('selectmain')
        
        if 'images' in request.FILES:
            obj.images=request.FILES['images']
            print('................image fetch.....................')
        if 'img1' in request.FILES:
            obj.img1=request.FILES['img1']
            print('................image fetch.....................')
        if 'img2' in request.FILES:
            obj.img2=request.FILES['img2']
            print('................image fetch.....................')
        if 'img3' in request.FILES:
            obj.img3=request.FILES['img3']
            print('................image fetch.....................')
        if int(obj.stock) < 0:
            print('.................saved...........................')
            obj.is_available=False
            return redirect('product')
        else:
            obj.is_available=True
        obj.save()
        messages.success(request,"New Product Added!")
        return redirect('product')
    print('.............showing product add page............')
    return redirect('add_product_page')

def prdt_edit_page(request):
    main=Main_Category.objects.all()
    sub_cat=Sub_Category.objects.all()
    # product=Product.objects.all()
    context={
        'main':main,
        'sub_cat':sub_cat,
    }
    return render(request,'adminapp/product_edit.html',context)

def prdt_edit(request,id):
    main=Main_Category.objects.all()
    sub_cat=Sub_Category.objects.all()
    product=Product.objects.all()
    if request.method=='POST':
        product=Product.objects.get(pk=id)
        main=request.POST.get('selectmain')
        sub_cat=request.POST.get('selectsub')
        product_name=request.POST.get('productname')
        if Product.objects.filter(product_name=product_name).exists():
            print("exist cond working...........................")
            messages.error(request,'Already Exists')
            return redirect('prdt_edit')
        else:
            product.product_name=product_name
            product.slug=slugify(product_name)
            product.parent_main__prdt_id=main
            product.parent_sub__prdt_id=sub_cat
            product.save()
            print('updation work......................')
            messages.error(request,'ProductUpdated')
            return redirect('product')
    print('page showing................................')
    # return redirect('sub_cat_edit_page')
    return render(request,'adminapp/product_edit.html',{
         'product':product
    })



 




@login_required(login_url='admin_login')
def prdt_delete(request,id):
    prdt=Product.objects.filter(id=id).delete()
    return redirect('product')


