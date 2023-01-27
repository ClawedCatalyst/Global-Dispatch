from django.db import models
from hackSNU.models import New_User_Resgistration
# Create your models here.


class Business(models.Model):
    
    user = models.OneToOneField(New_User_Resgistration, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)


class WareHouse(models.Model):
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    max_capacity = models.PositiveBigIntegerField()
    present_capacity = models.PositiveBigIntegerField(default = 0)
    location = models.CharField(max_length=255)
    
    
class Category(models.Model):
    
    name = models.CharField(max_length=255)
    

class Commodity(models.Model):
    
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique = True)
    quantity = models.PositiveBigIntegerField()
    volume = models.PositiveBigIntegerField()
    