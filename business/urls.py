from django.urls import path
from .views import *

urlpatterns = [
    
    path('warehouse/', WarehouseView.as_view()),
    path('warehouse/<int:pk>/', SingleWarehouseView.as_view()),
    path('commodity/', CommodityView.as_view()),
    path('commodity/<int:pk>/', SingleCommodityView.as_view()),
    path('category/', CategoryView.as_view()),
    path('category/<int:pk>/', SingleCategoryView.as_view()),
]