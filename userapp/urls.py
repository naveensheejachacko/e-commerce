from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('user_login/',views.user_login,name='user_login'),
    path('signup/',views.user_signup,name='signup'),
    path('user_logout',views.user_logout,name='user_logout'),


    path('otp_login/',views.otp_login,name='otp_login'),
    path('otp_login_page/',views.otp_login_page,name='otp_login_page'),
    path('enter_otp/',views.enter_otp,name='enter_otp'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
]
