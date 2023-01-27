from rest_framework.generics import *
from business.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from django.shortcuts import get_object_or_404



class BusinessView(CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessSerializer
    
    def post(self, request, *args, **kwargs):
        request.data.update({"user": self.request.user.id})
        return super().post(request, *args, **kwargs)
    
    
class WarehouseView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSerializer
    
    
    def get_queryset(self):
        user = self.request.user.id
        business = get_object_or_404(Business, user = user)
        return WareHouse.objects.filter(business = business)


    def post(self, request, *args, **kwargs):
        business = get_object_or_404(Business, user = self.request.user.id)
        request.data.update({"business": business.id})
        print(request.data)
        return super().post(request, *args, **kwargs)
    
class SingleWarehouseView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSerializer
    
    
    def get_queryset(self):
        user = self.request.user
        business = get_object_or_404(Business, user = user)
        return WareHouse.objects.filter(business = business)
    
    
class CategoryView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    
    
    def get_queryset(self):
        return Category.objects.all()

            
    
class SingleCategoryView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    
    
    def get_queryset(self):
        return Category.objects.all()
    
    
class CommodityView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommoditySerializer
    
    
    def get_queryset(self):
        user = self.request.user
        id = self.request.GET.get('warehouse')
        business = get_object_or_404(Business, user = user)
        warehouse = get_object_or_404(WareHouse, business = business, id = id)
        return Commodity.objects.filter(warehouse = warehouse)
        
    
    
class SingleCommodityView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = CommoditySerializer
    
    
    def get_queryset(self):
        return Commodity.objects.all()
        
    
    

        
    
    