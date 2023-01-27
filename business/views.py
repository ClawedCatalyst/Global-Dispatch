import encodings
from unittest.result import failfast
from rest_framework.generics import *
from business.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from django.shortcuts import get_object_or_404
from hackSNU.models import *
import pickle
import numpy as np
model = pickle.load(open('model/modell.pkl','rb'))
from rest_framework.response import Response


class BusinessView(CreateAPIView,ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessSerializer
    
    def get_queryset(self):
        user = self.request.user.id
        user = get_object_or_404(New_User_Resgistration, id = user)
        print(user)
        return Business.objects.filter(user = user)
        
    
    
    def post(self, request, *args, **kwargs):
        request.data.update({"user": self.request.user.id})
        return super().post(request, *args, **kwargs)
    
    
class WarehouseView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = WarehouseSerializer
    
    
    def get_queryset(self):
        predict()
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


class MlDataPredict(CreateAPIView):
    
    def post(self,request):
        quantity = float(request.data.get('quantity'))
        volumn = float(request.data.get('volumn'))
        distfromIndia = float(request.data.get('dist'))
        
        fv = [quantity,volumn,distfromIndia]
        fv = np.array(fv).reshape((1,-1))
        p = model.predict(fv)
        
        return Response({'Predicted Price':p})
    

    
    
        
    
    

        
    
    