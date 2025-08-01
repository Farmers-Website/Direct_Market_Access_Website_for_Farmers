
from django.shortcuts import render
from django.urls import path
from . import views
from .views import Login,register,customer_product,CartView,FeedbackView,ProfileView

from .middlewares.auth import  auth_middleware

urlpatterns = [
    path('home/', views.customer_home, name='customer_home'),
    path('register/', register.as_view(), name='customer_register'),
    path('login/',Login.as_view(),name='customer_login'),
   
   path('products/', auth_middleware(customer_product.as_view()), name='product_listing'),
   path('cart/', auth_middleware(CartView.as_view()), name='cart'),
   path('checkout/', auth_middleware(views.checkout), name='checkout'),
   path('order/history/', auth_middleware(views.order_history), name='order_history'),
   path('feedback/', auth_middleware(FeedbackView.as_view()), name='feedback'),
   path('profile/', auth_middleware(ProfileView.as_view()), name='profile'),
   path('logout/', views.logout_view, name='logout'),


   

]