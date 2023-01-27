from rest_framework import serializers, status
from .models import *
from business.models import *
from django.shortcuts import get_object_or_404





class BusinessSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Business
        fields = "__all__"
        

class WarehouseSerializer(serializers.ModelSerializer):
    
    business = BusinessSerializer(source = 'business', read_only = True)
    
    class Meta:
        model = WareHouse
        fields = "__all__"
        
    
    
class CommoditySerializer(serializers.ModelSerializer):
    
    warehouse = WarehouseSerializer(source = 'warehouse', read_only = True)
    
    class Meta:
        model = Commodity
        fields = "__all__"
    
    
class CategorySerializer(serializers.ModelSerializer):
    
    commodity = CommoditySerializer(read_only = True)
    
    class Meta:
        model = Category
        fields = "__all__"
    
    
        