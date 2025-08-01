from django.db import models
from .farmers import Farmer
from .categories import Category





class Product(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/products/')
    quantity=models.DecimalField(max_digits=20, decimal_places=2)
    

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()
        
    def __str__(self):
        return self.name
    
    def reduce_stock(self, order_quantity):
        if self.quantity >= order_quantity:
            self.quantity -= order_quantity
            self.save()
            return True
        return False