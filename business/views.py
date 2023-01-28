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
    

class ShipmentView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer
    
    
    def get_queryset(self):
        business = get_object_or_404(Business, user = self.request.user)
        warehouses = business.warehouse_set.all()
        queryset = WareHouse.objects.none()
        for warehouse in warehouses:
            queryset = queryset.union(warehouse.sent_shipments.all())
            
        for warehouse in warehouses:
            queryset = queryset.union(warehouse.received_shipments.all())
        queryset = queryset.order_by('-id')
        return queryset

   
class SingleShipmentView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()



class SearchShipmentView(views.APIView):
    
    def post(self, request, *args, **kwargs):
        
        hash = request.data.get('hash')
        if hash is None:
            return Response({"detail": "PLease provide the hash for tracking the shipment"})

        shipment = get_object_or_404(Shipment, hash = hash)
        
        return Response(ShipmentSerializer(instance = shipment, context = {'request':self.request}).data, status= status.HTTP_200_OK)
        

class MlDataPredict(CreateAPIView):
    
    def post(self,request):
        quantity = float(request.data.get('quantity'))
        volumn = float(request.data.get('volumn'))
        distfromIndia = float(request.data.get('dist'))
        
        fv = [quantity,volumn,distfromIndia]
        fv = np.array(fv).reshape((1,-1))
        p = model.predict(fv)
        
        return Response({'Predicted Price':p})

class GetAllBusiness(ListAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Business.objects.filter().exclude(user=self.request.user.id)
    
    

class WareHouseView(ListAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        business = self.request.GET.get('bus')
        return WareHouse.objects.filter(business=business)
    
class AdminShipmentView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer
    
    def get(self,request):
        if request.user.isAdmin == True:
            shipment = Shipment.objects.all().order_by('-id')
            serializer = self.serializer_class(shipment,many=True)
            return Response(serializer.data)
        return Response({'msg':'Not Admin'})

class ShipmentApproval(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShipmentSerializer
    
    def get(self,request):
        if request.user.isAdmin == True:
            shipment = Shipment.objects.filter().exclude(status='approved').order_by('-id')
            serializer = self.serializer_class(shipment,many=True)
            return Response(serializer.data)
        return Response({'msg':'Not Admin'})
    
    def put(self,request):
        if request.user.isAdmin == True:
            shipment = Shipment.objects.get(id=request.data.get('shipID'))
            if shipment.status == 'Approved':
                return Response({'msg':'Shipment is Approved'})
            else:
                serializer = self.serializer_class(instance=shipment, data = request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    print(serializer.data['destination'])
                    if  serializer.data['destination_country'] != 'nothing':
                        shipment.destination = None
                        shipment.save()
                    if  serializer.data['destination']['location'] != '':
                        shipment.destination_country = None
                        shipment.save()
                    source_location = shipment.source.location[-3:]
                    try:
                        destination_location = shipment.destination.location[-3:]
                    except:
                       pass
                    try:
                        destination_location = serializer.data['destination_country'][-3:]
                    except:
                           pass   
                     
                    try:
                        distance = calculate(source_location, destination_location)
                        expected_price = predict_price(shipment.quantity,shipment.commodity.volume, distance)
                        shipment.expected_price = expected_price
                        shipment.save()
                    except:
                        pass
                    serializer = self.serializer_class(shipment,many=False)
                    return Response(serializer.data)


        
    
    