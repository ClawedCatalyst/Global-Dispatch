from django.db import models
from hackSNU.models import New_User_Resgistration
from django.db.models.signals import post_save
import random, string
from django.dispatch import receiver
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
    
    
    
    
SHIPMENT_STATUS_CHOICES = {
    ('approved', 'approved'),
    ('not-approved', 'not-approved')
}
class Shipment(models.Model):
    
    source  = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name= "sent_shipments")
    destination  = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name= "received_shipments", blank=True, null = True)
    destination_country = models.CharField(max_length=255, blank = True , null = True)
    hash = models.CharField(max_length = 255, blank = True)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    status = models.CharField(max_length = 255, choices = SHIPMENT_STATUS_CHOICES, default = "not-approved")
    expected_price = models.PositiveBigIntegerField(default = 0)
    final_price = models.PositiveBigIntegerField(blank = True, null = True)
    
@receiver(post_save, sender = Shipment)

def set_default_hash(sender, instance, created, **kwargs):
    
    if created: 
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        instance.hash = rand
        instance.save()
    
    
    
    