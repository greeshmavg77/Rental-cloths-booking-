from django.urls import path

from .import views


urlpatterns=[
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('product',views.product,name='product'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart', views.cart, name='cart'),
    path('remove', views.remove, name='remove'),
    path('view_cart', views.view_cart, name='view_cart'),
    path('payment',views.payment,name='payment'),
    path('success',views.success,name='success'),
    path('admin_additem',views.admin_additem,name='admin_additem'),
    path('item_view',views.item_view, name='item_view'),
    path('remove_item',views.remove_item,name='remove_item'),
    path('email',views.email,name='email'),
    path('user-list/', views.user_list, name='user_list'),
]