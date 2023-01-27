import encodings
from unittest.result import failfast
from rest_framework.generics import *
from business.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from hackSNU.models import *
import pickle
import numpy as np
model = pickle.load(open('model/modell.pkl','rb'))
from rest_framework.response import Response


class BusinessView(CreateAPIView,ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessSerializer
    
    def get_object(self):
        return get_object_or_404(Business, user = self.request.user)
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
    
    
    
    def post(self, request, *args, **kwargs):
        
        return super().post(request, *args, **kwargs)
    
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
    

class SendShipmentView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer
    
    
    def get_queryset(self):
        business = get_object_or_404(Business, user = self.request.user)
        warehouses = business.warehouse_set.all()
        queryset = WareHouse.objects.none()
        for warehouse in warehouses:
            queryset = queryset.union(warehouse.sent_shipments.all())
        return queryset

    
class ReceiveShipmentView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer
    
    
    def get_queryset(self):
        business = get_object_or_404(Business, user = self.request.user)
        warehouses = business.warehouse_set.all()
        queryset = WareHouse.objects.none()
        
        for warehouse in warehouses:
            queryset = queryset.union(warehouse.received_shipments.all())
        return queryset



class SearchShipmentView(views.APIView):
    
    def post(self, request, *args, **kwargs):
        
        hash = request.data.get('hash')
        if hash is None:
            return Response({"detail": "PLease provide the hash for tracking the shipment"})

        shipment = get_object_or_404(Shipment, hash = hash)
        
        


class MlDataPredict(CreateAPIView):
    
    def post(self,request):
        quantity = float(request.data.get('quantity'))
        volumn = float(request.data.get('volumn'))
        distfromIndia = float(request.data.get('dist'))
        
        fv = [quantity,volumn,distfromIndia]
        fv = np.array(fv).reshape((1,-1))
        p = model.predict(fv)
        
        return Response({'Predicted Price':p})
    

    
    
        
    
    

        
    
    