
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import  product_feedback_view, view_orders,accept_order
from .views import update_product,add_product,delete_product,view_product,Farmer_dashboard,Login,Register,farmer_profile,edit_farmer_profile,logout

urlpatterns = [
    path('<int:id>/',Farmer_dashboard.as_view(),name='farmer_dashboard'),
    path('login/',Login.as_view(),name='farmer_login'),
    path('logout/', logout, name='logout'),
    path('register/',Register.as_view(),name='register'),
    path('profile/<int:id>/',farmer_profile, name='farmer_profile'),
    path('profile/edit/<int:id>/',edit_farmer_profile, name='edit_farmer_profile'),
    path('products/add_product/', add_product, name='add_product'),
    path('products/<int:product_id>/',view_product, name='view_product'),
    path('products/<int:product_id>/update_product/',update_product, name='update_product'),
    path('products/<int:product_id>/delete_product/',delete_product, name='delete_product'),
    path('orders/<int:id>/',view_orders, name='farmer_orders'),
    path('accept_order/<int:id>/',accept_order, name='accept_order'),
   path('product/<int:product_id>/feedback/', product_feedback_view, name='product_feedback'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)