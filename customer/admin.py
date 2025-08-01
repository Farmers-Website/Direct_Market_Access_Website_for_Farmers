
from django.contrib import admin

from .models.category import Category
from .models.customer import Customer
from .models.order import Order
from .models.feedback import Feedback






class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


# Register your models here.

admin.site.register(Category , AdminCategory)
admin.site.register(Customer )
admin.site.register(Order )
admin.site.register(Feedback)