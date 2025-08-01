from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product_list/', views.product_list, name='product_list'),  
]
