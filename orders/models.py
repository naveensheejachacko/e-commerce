
from django.db import models
from account.models import Account
from categories.models import Product
from userapp.models import Address



class Order(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=250,null=True)
    orderstatuses=(
        ('pending','pending'),
        ('out for shipping','out for shipping'),
        ('completed','completed'),
    )
    status=models.CharField(max_length=150,choices=orderstatuses,default='Pending')
    
    tracking_no=models.CharField(max_length=150,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return'{}-{}'.format(self.id,self.tracking_no)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)
    status=models.CharField(max_length=150,default='Pending')
    
    def __str__(self):
        return '{} {}'.format(self.order.id,self.order.tracking_no)
