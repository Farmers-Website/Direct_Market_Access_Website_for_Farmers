from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    vendor=models.ForeignKey(User,on_delete=models.CASCADE)
    title =models.CharField(max_length=200)
    descripton=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at =models.DateTimeField(auto_now_add=True)

    
class MarketDetail(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    market_trend=models.CharField(max_length=100)
    pricing_info=models.TextField()