from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('user_manage/',views.user_manage,name='user_manage'),
    path('block_user/<int:bid>/', views.block_user, name="block_user"),
]
