from django.urls import path
from .views import *

urlpatterns = [
    
    path('', BusinessView.as_view()),
    path('getallBus/',GetAllBusiness.as_view()),
    path('getwarehouse/',WareHouseView.as_view()),
    path('warehouse/', WarehouseView.as_view()),
    path('warehouse/<int:pk>/', SingleWarehouseView.as_view()),
    path('category/', CategoryView.as_view()),
    path('category/<int:pk>/', SingleCategoryView.as_view()),
    path('commodity/', CommodityView.as_view()),
    path('commodity/<int:pk>/', SingleCommodityView.as_view()),
    path('predict/',MlDataPredict.as_view()),
    
    path('shipment/', ShipmentView.as_view()),
    path('shipment/<int:pk>/', SingleShipmentView.as_view()),
    # path('shipment/received/', ReceiveShipmentView.as_view()),
    path('shipment/search/', SearchShipmentView.as_view()),
    
]