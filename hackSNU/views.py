from rest_framework import generics,status
from rest_framework.response import Response
from . models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .utils import *


# API for sending OTP.   
class OTP_send(generics.CreateAPIView):
    serializer_class = OTP_Serializer
    
# OTP verification API.    
class Verify_OTP(generics.CreateAPIView):
    serializer_class = OTPVerifySerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Email Verified'}, status=status.HTTP_200_OK)

# Registration API
class New_user_registration(generics.CreateAPIView):
    serializer_class = NewUserSerializer
    
    
    
class LoginView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    