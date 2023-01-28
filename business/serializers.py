from dataclasses import fields
from rest_framework import serializers, status
from .models import *
from business.models import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from hackSNU.models import *
from hackSNU.serializers import *
from business.temp import calculate, predict_price
class BusinessSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Business
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = NewUserSerializer(instance = instance.user).data
        return data
        

class WarehouseSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = WareHouse
        fields = "__all__"
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['business'] = BusinessSerializer(instance = instance.business).data
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
        if warehouse.present_capacity + data['quantity'] * data['volume'] > warehouse.max_capacity:
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
    
        
        
class ShipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shipment
        fields = "__all__"
        
        
    
    def validate(self, attrs):
        data =  super().validate(attrs)
        commodity = get_object_or_404(Commodity, id = data['commodity'].id)
        
        if commodity.quantity < data['quantity']:
            raise ValidationError("You don't have enough quantity in the warehouse")
        
        source_location = data['source'].location[-3:]
        try:
            destination_location = data['destination'].location[-3:]
        except KeyError:
            destination_location = data['destination_country'][-3:]
        except Exception as e:
            raise e
        
        distance = calculate(source_location, destination_location)
        expected_price = predict_price(data['quantity'],data['commodity'].volume, distance)
        data['expected_price'] = expected_price
        return data
        
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user =  self.context['request'].user
        business = get_object_or_404(Business, user = user)
        warehouses = business.warehouse_set.all()
        
        if warehouses.filter(id = instance.source.id).exists():
            data['send'] = True
        else:
            data['send'] = False
            
        data['source'] = WarehouseSerializer(instance.source).data
        data['destination'] = WarehouseSerializer(instance.destination).data
        data['commodity'] = CommoditySerializer(instance.commodity).data
        return data

    
    def create(self, validated_data):
        shipment = super().create(validated_data)
        
        commodity = shipment.commodity
        commodity.quantity -= shipment.quantity
        commodity.save()
        
        source_warehouse = shipment.source
        source_warehouse.present_capacity -= shipment.quantity
        source_warehouse.save()
        
        return shipment
    
    
    
