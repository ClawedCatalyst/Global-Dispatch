from django.urls import path
from . views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('otp/' ,OTP_send.as_view()),
    path('otp_verify/', Verify_OTP.as_view()),
    path('registration/' ,New_user_registration.as_view()),
    path('login/' ,LoginView.as_view()),
]