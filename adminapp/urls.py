from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('user_manage/',views.user_manage,name='user_manage'),
    path('block_user/<int:bid>/', views.block_user, name="block_user"),



    path('activeorders/',views.activeorders,name='activeorders'),
    path('order_history/',views.order_history,name='order_history'),
    path('order_status_change',views.order_status_change,name='order_status_change'),


#offer and Coupon

    path('category_offer',views.category_offer,name='category_offer'),
    path('add_category_offer',views.add_category_offer,name='add_category_offer'),
    path('edit_category_offer/<int:id>/',views.edit_category_offer,name='edit_category_offer'),
    path('delete_category_offer/<int:id>/',views.delete_category_offer,name='delete_category_offer'),
    
    path('subcategory_offer',views.subcategory_offer,name='subcategory_offer'),
    path('add_subcategory_offer',views.add_subcategory_offer,name='add_subcategory_offer'),
    # path('edit_subcategory_offer',views.edit_subcategory_offer,name='edit_subcategory_offer'),
    path('delete_subcategory_offer/<int:id>/',views.delete_subcategory_offer,name='delete_subcategory_offer'),

    path('product_offer',views.product_offer,name='product_offer'),
    path('add_product_offer',views.add_product_offer,name='add_product_offer'),
    # path('edit_product_offer',views.edit_product_offer,name='edit_product_offer'),
    path('delete_product_offer/<int:id>/',views.delete_product_offer,name='delete_product_offer'),

    path('coupons/',views.coupons,name='coupons'),
    path('add_coupons/',views.add_coupons,name='add_coupons'),
    path('delete_coupons/<int:id>/',views.delete_coupons,name='delete_coupons'),



    # Reports
    path('product_report/',views.product_report,name='product_report'),
    path('product_csv/',views.product_csv,name='product_csv'),
    path('generateProductPdf',views.generateProductPdf.as_view(),name='generateProductPdf'),
    path('product_excel',views.product_excel,name='product_excel'),

    path('salesReport/',views.salesReport,name='salesReport'),
    path('by_date/',views.by_date,name='by_date'),
    path('generatesalesReportPdf',views.generatesalesReportPdf.as_view(),name='generatesalesReportPdf'),
    path('by_month/',views.by_month,name='by_month'),
    path('by_year/',views.by_year,name='by_year')


]


