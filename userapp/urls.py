from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('otp_login/',views.otp_login,name='otp_login'),
    path('otp_login_page/',views.otp_login_page,name='otp_login_page'),
    path('enter_otp/',views.enter_otp,name='enter_otp'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),


    path('signup/',views.user_signup,name='signup'),
    path('signup_otp/',views.signup_otp,name='signup_otp'),
    path('verify_signup_otp/',views.verify_signup_otp,name='verify_signup_otp'),



    path('dashboard/',views.dashboard,name='dashboard'),
    
    path('add_to_wishlist/<int:id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('user_wishlist/',views.user_wishlist,name="user_wishlist"),

    # path('userprofile/', views.userprofile, name='userprofile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    # path('user_orders/',views.user_orders,name='user_orders'),
    path('order_summary/',views.order_summary,name='order_summary'),
    path('orderview/<int:id>',views.orderview,name='orderview'),

    path('generateinvoice/<int:id>/',views.generateInvoice.as_view(), name = 'generateinvoice'),
    path('cancel_order/<int:pk>/',views.cancel_order,name='cancel_order'),
    path('return_order/<int:id>/',views.return_order,name='return_order'),
    path('accept_return/<int:id>/',views.accept_return,name='accept_return'),

    path('view_address/',views.view_address,name='view_address'),
    path('add_address/',views.add_address,name='add_address'),
    path("delete-address/<int:pk>/",views.delete_address,name="delete-address"),



    
]



