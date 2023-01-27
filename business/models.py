from django.db import models

# Create your models here.


class Business(models.Model):
    
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)


class WareHouse(models.Model):
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    max_capacity = models.PositiveBigIntegerField()
    present_capacity = models.PositiveBigIntegerField(default = 0)
    location = models.CharField(max_length=255)
    
    
    
class Commodity(models.Model):
    
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    

class Category(models.Model):
    
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.PositiveBigIntegerField()
    volume = models.PositiveBigIntegerField()
    