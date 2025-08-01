from django.contrib import admin

# Register your models here.
from .models.farmers import Farmer
from .models.products import Product
from .models.categories import Category

# from .models.orders import Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name',)

# Customize Farmer Admin
@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'email', 'phone','image')


# Customize Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'category','image','farmer')
    search_fields = ('name', 'category')
    list_filter = ('category',)