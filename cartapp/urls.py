from django.urls import path
from . import views


    
    
urlpatterns = [  
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('delete_cart_item/<int:product_id>/<int:cart_item_id>/',views.delete_cart_item,name='delete_cart_item'),

    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),


    path('checkout/',views.checkout,name='checkout'),


   

]