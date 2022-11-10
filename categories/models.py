from tabnanny import verbose
from django.db import models
from django.urls import reverse

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
    
    def __str__(self):
        return self.product_name
    def get_url(self):
        return reverse("product_details",args=[self.parent_main_prdt.slug,self.parent_sub_prdt.slug,self.slug])
    