from rest_framework import status
from rest_framework.generics import *
from business.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView



class BusinessView(CreateAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BusinessSerializer
    
    
    
class WarehouseView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = WarehouseSerializer
    
    
    def get_queryset(self):
        user = self.request.user
        business = get_object_or_404(Business, user = user)
        return WareHouse.objects.filter(business = business)
    
    
    
class SingleWarehouseView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = WarehouseSerializer
    
    
    def get_queryset(self):
        user = self.request.user
        business = get_object_or_404(Business, user = user)
        return WareHouse.objects.filter(business = business)
    
    
    
class CommodityView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommoditySerializer
    
    
    def get_queryset(self):
        user = self.request.user
        business = get_object_or_404(Business, user = user)
        warehouse = get_object_or_404(WareHouse, business = business)
        return Commodity.objects.filter(warehouse = warehouse)
    
    
    
class SingleCommodityView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommoditySerializer
    
    
    def get_queryset(self):
        user = self.request.user
        business = get_object_or_404(Business, user = user)
        warehouse = get_object_or_404(WareHouse, business = business)
        return Commodity.objects.filter(warehouse = warehouse)
        
    
    
class CategoryView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    
    
    def get_queryset(self):
        user = self.request.user
        business = get_object_or_404(Business, user = user)
        warehouse = get_object_or_404(WareHouse, business = business)
        commodity = get_object_or_404(Commodity, warehouse = warehouse)
        return Category.objects.filter(commodity = commodity)
    
    
    
class SingleCategoryView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    
    
    def get_queryset(self):
        user = self.request.user
        business = get_object_or_404(Business, user = user)
        warehouse = get_object_or_404(WareHouse, business = business)
        commodity = get_object_or_404(Commodity, warehouse = warehouse)
        return Category.objects.filter(commodity = commodity)
        
    
    