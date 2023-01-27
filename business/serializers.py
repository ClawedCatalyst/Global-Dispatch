from rest_framework import serializers, status
from .models import *
from business.models import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

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
        
    def validate(self, attrs):
        data = super().validate(attrs)
        warehouse = get_object_or_404(WareHouse, id = data['warehouse'].id)
        if warehouse.present_capacity + data['quantity']*data['volume'] > warehouse.max_capacity:
            raise ValidationError("Warehouse overflown")
        return data
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data
        return data
        
    def create(self, validated_data):
        commodity = super().create(validated_data)
        warehouse = commodity.warehouse
        warehouse.present_capacity += (commodity.volume * commodity.quantity)
        warehouse.save()
        return commodity
    
        