from django.urls import path
from . import views
    
    
urlpatterns = [  
    path('',views.store,name='store'),
    path('<slug:maincategory_slug>/',
            views.store,
            name='products_by_maincategory'),
    path('<slug:maincategory_slug>/<slug:subcategory_slug>/',views.store,name='products_by_subcategory'),
    path('<slug:maincategory_slug>/<slug:subcategory_slug>/<slug:product_slug>/',
            views.product_details,
            name='product_details'),
    path('search',views.search,name='search'),
    path('filter_price',views.filter_price,name='filter_price'),

    path('load_size_user',views.load_size_user,name='load_size_user'),
  

]