

from django.db import models



class Customer(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=500)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    dob = models.DateField(blank=True, null=True)  # Date of Birth
    bio = models.TextField(blank=True, null=True)  # Optional bio
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)

    def register(self):
        self.save()

    def get_customer_by_email(email):
        try:
           return Customer.objects.get(email=email)
        except:
            False

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
