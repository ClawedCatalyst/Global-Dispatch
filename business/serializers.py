from dataclasses import fields
from rest_framework import serializers, status
from .models import *
from business.models import *
from django.shortcuts import get_object_or_404
from hackSNU.models import *
from hackSNU.serializers import *

class BusinessSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Business
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = NewUserSerializer(instance = instance.user).data
        print(data)
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
        
class GetAllDetailsSerializer(serializers.ModelSerializer):
    business = BusinessSerializer()
    
    class Meta:
        model = New_User_Resgistration
        fields = ['email','business']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['business'] = BusinessSerializer(user = instance.id).data
        # data['WareHouse'] = WareHouse(instance = data)
        return data