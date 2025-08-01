"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import settings
from django.shortcuts import redirect
from customer.views import home

from django_project import settings
from django.conf.urls.static import static



def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('product_listing')  
    else:
        return redirect('register')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('farmers/',include('farmers.urls')),
    path('',home,name='home'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
