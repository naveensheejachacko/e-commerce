from django.urls import path
from . import views



    
    
urlpatterns = [  
    path('place_order/',views.place_order,name='place_order'),
    # path('cod/',views.cod,name='cod'),
    # path('Razorpay/',views.Razorpay,name='Razorpay'),
    # path('summary',views.summary,name='summary'),
    path('proceed_to_pay',views.proceed_to_pay,name='proceed_to_pay'),
]

