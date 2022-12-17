from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
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
#paginator
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger 





#offer

from offer.models import CategoryOffer,Coupon,SubcategoryOffer,ProductOffer
from offer.forms import CategoryOfferForm,SubcategoryOfferForm,ProductOfferForm,CouponForm


#Report

from django.http import HttpResponse
from xhtml2pdf import pisa
from django.views.generic import View
from django.template.loader import get_template
import xlwt
import csv
from io import BytesIO

from store.forms import BannerForm, EditBanner
from store.models import Banners
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

        products = Product.objects.all()
        total_users=Account.objects.filter(Q(is_active=True)& Q(is_admin=False)).count()
        day=datetime.datetime.now()
        visitors=Account.objects.filter(last_login=day).count()

        total_revenue=OrderItem.objects.filter(status='Delivered').aggregate(Sum('price'))
        total_orders=OrderItem.objects.filter(status='Delivered').count()
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



@login_required(login_url='admin_login')
def activeorders(request):
    
    exclude_list = [
        "Delivered",
        "Cancelled",
        "Refund Initiated",
        "Cancelled_item",
        
    ]
    active_orders =OrderItem.objects.all().exclude(
        status__in=exclude_list
    ).order_by('-id')#for reversing order
    status=STATUS1
    paginator=Paginator(active_orders,5)
    page=request.GET.get('page')
    paged_orders_list=paginator.get_page(page) 

    

    context ={
        "active_orders":active_orders,
        "status":status,
        'active_orders':paged_orders_list
    }
    return render(request,'adminapp/active_orders.html',context)

@login_required(login_url='admin_login')
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
    paginator=Paginator(active_orders,10)
    page=request.GET.get('page')
    paged_orders_list=paginator.get_page(page) 

  
    


    context = {
        "active_orders": active_orders,
        "status": status,
        "active_orders":paged_orders_list,
   
        
    }
    return render(request, "adminapp/order_history.html", context)

@login_required(login_url='admin_login')
def order_status_change(request):
    id = request.POST['id']
    status = request.POST['status']
    order_item = OrderItem.objects.get(id=id)
    order_item.status = status
    order_item.save()
    return JsonResponse({"success": True})








#offer managemnet

@login_required(login_url='admin_login')
def category_offer(request):
    cat_offer=CategoryOffer.objects.all()
    return render(request,'adminapp/category_offer.html',{
        'cat_offer':cat_offer
    })
@login_required(login_url='admin_login')
def add_category_offer(request):
    form=CategoryOfferForm()
    if request.method=='POST':
        form=CategoryOfferForm(request.POST)
        discount=form.data['discount']
        if int(discount) <= 70:
            if form.is_valid():
                form.save()
                return redirect('category_offer')
            else:
                messages.error(request,'Already Exists!!')
                return redirect('add_category_offer')
        else:
            messages.error(request,'Percentage should be less than or equal to 70')
            return redirect('add_category_offer')
    context={
        'form':form
    }
    return render(request,'adminapp/add_category_offer.html',context)    

@login_required(login_url='admin_login')
def edit_category_offer(request,id):
    form=CategoryOfferForm()
    category_offer=get_object_or_404(CategoryOffer,id=id)
    

    form=CategoryOfferForm(request.POST,instance=category_offer)
    if form.is_valid():
        form.save()
        return redirect('category_offer')

    return render(request,'adminapp/edit_category_offer.html',{
        'form':form
    })

@login_required(login_url='admin_login')
def delete_category_offer(request,id):
    CategoryOffer.objects.filter(id=id).delete()
    return redirect('category_offer')


@login_required(login_url='admin_login')
def subcategory_offer(request):
    sub_offer=SubcategoryOffer.objects.all()
    return render(request,'adminapp/subcategory_offer.html',{
        'sub_offer':sub_offer
    })
@login_required(login_url='admin_login')
def add_subcategory_offer(request):
    form=SubcategoryOfferForm()
    if request.method=='POST':
        form=SubcategoryOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategory_offer')
    context={
        'form':form
    }
    return render(request,'adminapp/add_subcategory_offer.html',context)


@login_required(login_url='admin_login')
def delete_subcategory_offer(request,id):
    SubcategoryOffer.objects.filter(id=id).delete()
    return redirect('subcategory_offer')


@login_required(login_url='admin_login')
def product_offer(request):
    prdt_offer=ProductOffer.objects.all()
    return render(request,'adminapp/product_offer.html',{
        'prdt_offer':prdt_offer,
    })

@login_required(login_url='admin_login')  
def add_product_offer(request):
    form=ProductOfferForm()
    if request.method=='POST':
        form=ProductOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_offer')
    context={
        'form':form
    }
    return render(request,'adminapp/add_product_offer.html',context)
@login_required(login_url='admin_login')
def delete_product_offer(request,id):
    ProductOffer.objects.filter(id=id).delete()
    return redirect('product_offer')



#banner

@login_required(login_url='admin_login')
def add_banner(request):
    form = BannerForm()
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("banner")
    context = {"form": form}
    return render(request, "adminapp/banner_add.html", context)

@login_required(login_url='admin_login')
def banner(request):
    banners = Banners.objects.all()
    
    return render(request, "adminapp/banner.html", {"banners": banners})


# def editbanner(request, banner_id):
#     edtbanner = Banners.objects.get(pk=banner_id)
#     form = EditBanner(instance=edtbanner)
#     if request.method == "POST":
#         form = EditBanner(request.POST, instance=edtbanner)
#         if form.is_valid():
#             try:
#                 form.save()

#             except:
#                 context = {"form": form}
#                 # messages.info(request,"A user with that email address already exists.")
#                 return render(request, "adminapp/editbanner.html", context)
#             return redirect("banner")

#     context = {"form": form}
#     return render(request, "adminapp/editbanner.html", context)



@login_required(login_url='admin_login')
def deletebanner(request, banner_id):
    bnr = Banners.objects.get(pk=banner_id)
    bnr.delete()
    messages.success(request, "Your Banner Has been deleted")
    return redirect("banner")





#coupon management 


@login_required(login_url='admin_login')
def coupons(request):
    coupons=Coupon.objects.all()
    return render(request,'adminapp/coupons.html',{
        'coupons':coupons
    })


@login_required(login_url='admin_login')
def add_coupons(request):
    form=CouponForm()
    if request.method=='POST':
        form=CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupons')
    else:
        print('error')
    
    return render(request,'adminapp/add_coupons.html',{
        'form':form
    })

@login_required(login_url='admin_login')
def delete_coupons(request,id):
    Coupon.objects.filter(id=id).delete()
    return redirect('coupons')


@login_required(login_url='admin_login')
def product_report(request):
    products=Product.objects.all()
    

    if request.GET.get('from'):
        product_date_from=datetime.datetime.strptime(request.GET.get('from'),"%Y-%m-%d")
        product_date_to=datetime.datetime.strptime(request.GET.get('to'),"%Y-%m-%d")

        product_date_to+=datetime.timedelta(days=1)
        products=Product.objects.filter(added_date__range=[product_date_from,product_date_to])    
    return render(request,'adminapp/product_report.html',{
        'products':products,
        
        
    })



@login_required(login_url='admin_login')
def product_csv(request):
    response=HttpResponse(content_type='text/csv')
    response[
        "Content-Disposition"
    ] = "attachement; filename=Product_Report.csv"

    writer=csv.writer(response)
    writer.writerow(
        [
            "Product Name",
            "Main Category Name",
            "Sub Category Name",
            "Price"
            "Stock"
        ]
    )
    products=Product.objects.all().order_by('id')
    for p in products:
        writer.writerow(
            [
                p.product_name,
                p.parent_main_prdt.main_category_name,
                p.parent_sub_prdt.sub_cat_name,
                p.price,
                p.stock,
            ]
        )
    return response



class generateProductPdf(View):
    def get(self,request,*args,**kwargs):
        try:
            products=Product.objects.all()
            
        except:
            return HttpResponse("505 not found")
        data={
            'products':products
        }
        pdf=render_to_pdf('adminapp/product_pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')

def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def product_excel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response[
        "Content-Disposition"
    ] = "attachement; filename=Product_Report.xls"
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Product_Data')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True

    columns=[
            "Product Name",
            "Main Category Name",
            "Sub Category Name",
            "Price",
            "Stock"
    ]

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style=xlwt.XFStyle()
    rows=Product.objects.all().values_list('product_name','parent_main_prdt','parent_sub_prdt','price','stock')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)

    wb.save(response)
    return response


    

def salesReport(request):
    orders=Order.objects.all()
    new_order_list=[]

    for i in orders:
        order_items=OrderItem.objects.filter(order_id=i.id)
        for j in order_items:
            item={
                'id':i.id,
                'ordered_date':i.created_at,
                'user':i.user,
                'price':j.price,
                'method':i.payment_mode,
                'status':j.status,


            }
            new_order_list.append(item)
    # paginator=Paginator(new_order_list,10)
    # page=request.GET.get('page')
    # paged_orders_list=paginator.get_page(page)  
    return render(request,'adminapp/salesReport.html')
        
  
    # return render(request,'adminapp/salesReport.html',{
    #     'order':paged_orders_list,
    # })

def by_date(request):
    if request.GET.get('from'):
        sales_date_from=datetime.datetime.strptime(request.GET.get('from'),"%Y-%m-%d")
        sales_date_to=datetime.datetime.strptime(request.GET.get('to'),"%Y-%m-%d")

        sales_date_to+=datetime.timedelta(days=1)
        orders=Order.objects.filter(created_at__range=[sales_date_from,sales_date_to])

        new_order_list=[]

        for i in orders:
            order_items=OrderItem.objects.filter(order_id=i.id)
            for j in order_items:
                item={
                    'id':i.id,
                    'ordered_date':i.created_at,
                    'user':i.user,
                    'price':j.price,
                    'method':i.payment_mode,
                    'status':j.status,


                }
                new_order_list.append(item)
    else:
        messages.error(request,'Please select date')
        return redirect('salesReport')
    return render(request,'adminapp/salesReport.html',{
        'order':new_order_list,
    })

class generatesalesReportPdf(View):
    def get(self,request,*args,**kwargs):
        try:
            orders=Order.objects.all()
            new_order_list=[]

            for i in orders:
                order_items=OrderItem.objects.filter(order_id=i.id)
                for j in order_items:
                    item={
                        'id':i.id,
                        'ordered_date':i.created_at,
                        'user':i.user,
                        'price':j.price,
                        'method':i.payment_mode,
                        'status':j.status,


                    }
                    new_order_list.append(item)
                    
        except:
            return HttpResponse("505 not found")
        data={
            'order':new_order_list
        }
        pdf=render_to_pdf('adminapp/salesReport_pdf.html',data)
        return HttpResponse(pdf,content_type='application/pdf')



def by_month(request):
    month=request.POST.get('month')
    orders=Order.objects.filter(created_at__month=month)
    new_order_list=[]

    for i in orders:
        order_items=OrderItem.objects.filter(order_id=i.id)
        for j in order_items:
            item={
                'id':i.id,
                'ordered_date':i.created_at,
                'user':i.user,
                'price':j.price,
                'method':i.payment_mode,
                'status':j.status,


            }
            new_order_list.append(item)
        
    return render(request,'adminapp/salesReport.html',{
        'order':new_order_list,
    })

def by_year(request):
    year=request.POST.get('year')
    orders=Order.objects.filter(created_at__year=year)
    new_order_list=[]

    for i in orders:
        order_items=OrderItem.objects.filter(order_id=i.id)
        for j in order_items:
            item={
                'id':i.id,
                'ordered_date':i.created_at,
                'user':i.user,
                'price':j.price,
                'method':i.payment_mode,
                'status':j.status,


            }
            new_order_list.append(item)
        
    return render(request,'adminapp/salesReport.html',{
        'order':new_order_list,
    })