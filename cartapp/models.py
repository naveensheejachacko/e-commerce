from django.db import models
from account.models import Account
from categories.models import Product, Variations

# Create your models here.

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.cart_id
class CartItem(models.Model):
    user            =models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    variations      =models.ManyToManyField(Variations, blank=True)
    product         =models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity        =models.IntegerField()
    cart            =models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    is_active       =models.BooleanField(default=True)
    coupon_discount=models.IntegerField(null=True)
    offer_discount=models.IntegerField(null=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
        
