from django.db import models
from django.contrib.auth.models import User

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmerprofile')
    # user_id = models.CharField(unique=True, null=True, blank=True, max_length=255)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/farmers/', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # Quantity available for sale by farmer

 

    def __str__(self):
        return self.name
    
    def register(self):
        self.save()

    @staticmethod
    def get_farmer_by_email(email):
        try:
            return Farmer.objects.get(email=email)
        except Farmer.DoesNotExist:
            return False
        
    def isExists(self):
            return Farmer.objects.filter(id=self.id).exists()
    
    
