from django.urls import path
from . import views
    
    
urlpatterns = [  
    path('main_category/',views.main_category,name='main_category'),

    path('add_main_cat/',views.add_main_cat,name='add_main_cat'),
    path('main_cat_add_page/',views.main_cat_add_page,name='main_cat_add_page'),
    path('edit_main_cat/<int:id>/',views.edit_main_cat,name='edit_main_cat'),
    path('main_cat_delete/<int:id>',views.main_cat_delete,name='main_cat_delete'),
    # path('main_cat_up/',views.main_cat_up,name='main_cat_up'),

    path('sub_category/',views.sub_category,name='sub_category'),
    path('subcat_add/',views.subcat_add,name='subcat_add'),
    path('sub_cat_add_page/',views.subcat_add_page,name='sub_cat_add_page'),
    path('sub_cat_edit_page/',views.sub_cat_edit_page,name='sub_cat_edit_page'),
    path('sub_cat_edit/<int:id>/',views.sub_cat_edit,name='sub_cat_edit'),
    path('sub_cat_delete/<int:id>',views.sub_cat_delete,name='sub_cat_delete'),

    path('product/',views.product,name='product'),
    path('add_product/',views.add_product,name='add_product'),

    path('add_product_page/',views.add_product_page,name='add_product_page'),
    path('subcataddproduct/<int:catid>/',views.load_subcategory,name='load_subcategory'),
    path('dropdown_P',views.dropdown_P,name='dropdown_P'),
    path('prdt_edit_page',views.prdt_edit_page,name='prdt_edit_page'),
    path('prdt_edit/<int:id>/',views.prdt_edit,name='prdt_edit'),

    path('prdt_delete/<int:id>',views.prdt_delete,name='prdt_delete'),


    # Product Varaition
    path('add_size/',views.add_size,name='add_size'),
    path('add_color/',views.add_color,name='add_color'),
    path('variations/',views.variations,name='variations'),
    path('add_variations/<int:id>/',views.add_variations,name='add_variations'),
    path('load_size/',views.load_size,name='load_size'),



]