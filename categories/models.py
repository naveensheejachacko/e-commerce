from tabnanny import verbose
from django.db import models
from django.urls import reverse


from django.utils import timezone
from django.conf import settings
from random import choices


from django.apps import apps
from django.db.models.aggregates import Sum

# Create your models here.

class Main_Category(models.Model):
    main_category_name  =models.CharField(max_length=100,unique=True)
    slug                =models.SlugField(max_length=100,unique=True)
    thumbnail          =models.ImageField(upload_to='photos/thumbanil', blank=True)
    
    def __str__(self):
        return self.main_category_name
    def get_url(self):
        return reverse('products_by_maincategory',args=[self.slug])

class Sub_Category(models.Model):
    sub_cat_name       =models.CharField(max_length=100,unique=True)
    slug               =models.SlugField(max_length=100,unique=True)
    parent_main         =models.ForeignKey(Main_Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_cat_name
    def get_url(self):
        return reverse('products_by_subcategory',args=[self.parent_main.slug,self.slug])
    
    
class Product(models.Model):
    product_name       =models.CharField(max_length=300,unique=True,blank=False)
    slug               =models.SlugField(max_length=300,unique=True,blank=False,null=True,default='')
    prdt_desc          =models.TextField(null=True)
    price              =models.IntegerField(null=False)
    images             =models.ImageField(upload_to='product/images',blank=False)
    img1               =models.ImageField(upload_to='product/images',blank=True)
    img2               =models.ImageField(upload_to='product/images',blank=True)
    img3               =models.ImageField(upload_to='product/images',blank=True)
    stock              =models.IntegerField(null=True)
    is_available       =models.BooleanField(default=False)
    created_date       =models.DateTimeField(auto_now_add=True)
    modified_date      =models.DateTimeField(auto_now_add=True)
    parent_main_prdt   =models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    parent_sub_prdt    =models.ForeignKey(Sub_Category,on_delete=models.CASCADE)
    users_wishlist     =models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='users_wishlist',blank=True)
    def __str__(self):
        return self.product_name
    def get_url(self):
        return reverse("product_details",args=[self.parent_main_prdt.slug,self.parent_sub_prdt.slug,self.slug])
    
    def get_revenue(self,month=timezone.now().month):
        orderitems=apps.get_model("orders",'OrderItem')
        orders=orderitems.objects.filter(product=self,created_at__month=month,status="Delivered")
        return orders.values("product").annotate(revenue=Sum("price"))

    def get_profit(self,month=timezone.now().month):
        orderitems=apps.get_model("orders",'OrderItem')
        orders=orderitems.objects.filter(product=self,created_at__month=month,status="Delivered")
        calculating_profit=orders.values('product').annotate(profit=Sum('price'))
        profit=calculating_profit[0]['profit']*0.23
        return profit
        
    def get_count(self,month=timezone.now().month):
        orderitems=apps.get_model("orders",'OrderItem')
        orders=orderitems.objects.filter(product=self,created_at__month=month,status="Delivered")
        return orders.values("product").annotate(quantity=Sum("quantity"))



    def offer_price(self):
        try:
            if self.parent_main_prdt.categoryoffer.is_valid:
                offer_price=(self.price*(self.parent_main_prdt.categoryoffer.discount) / 100)
                new_price=self.price - offer_price
                return {
                    "new_price":new_price
                }
            raise
        except:
            try:
                if self.parent_sub_prdt.subcategoryoffer.is_valid:
                    offer_price=(self.price*(self.parent_sub_prdt.subcategoryoffer.discount) / 100)
                    new_price=self.price - offer_price
                    return {
                        "new_price":new_price
                    }
                raise
            except:
                try:
                    if  self.productoffer.is_valid:
                        offer_price=(self.price*(self.productoffer.discount) / 100)
                        new_price=self.price - offer_price
                        return {
                            "new_price":new_price
                        }
                    raise
                except:
                    return {
                            "new_price":self.price
                        }
            



class Color(models.Model):
    color_value=models.CharField(max_length=50,null=True)


class Size(models.Model):
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size_value=models.CharField(max_length=50,null=True)

class Variations(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE,null=True)
    color=models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
        
    def __str__(self):
        return self.color.color_value

