from rest_framework import serializers, status
from .models import *
from business.models import *
from django.shortcuts import get_object_or_404


class BusinessSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Business
        fields = "__all__"
        

class WarehouseSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = WareHouse
        fields = "__all__"
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['business'] = BusinessSerializer(instance = instance.business,read_only = True).data
        return data
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
        
class CommoditySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Commodity
        fields = "__all__"
        
    
    
        