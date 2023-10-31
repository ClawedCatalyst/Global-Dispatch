import re
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .mail import send_otp
from .models import *
from .utils import *


class OTP_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ["email"]

    def validate(self, data):
        email = data["email"]
        if not re.findall("@.", email):
            raise ValidationError(("Enter a valid email"))
        user = list(New_User_Resgistration.objects.filter(email=email))
        if user != []:
            raise ValidationError({"msg": "User already exists"})
        return data

    def create(self, data):
        userOTP = OTP.objects.filter(email=data["email"])
        if userOTP is not None:
            print(userOTP)
            userOTP.delete()
        email = data["email"]
        OTP.objects.create(email=email)
        send_otp(email)

        return data


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    def validate(self, data):
        userOTP = OTP.objects.get(email=data["email"])

        if not userOTP.otp == data["otp"]:
            context = {"msg": "OTP incorrect"}
            raise ValidationError((context))
        if userOTP.time + timedelta(minutes=3) < timezone.now():
            context = {"msg": "OTP Timed Out"}
            userOTP.delete()
            raise ValidationError((context))
        userOTP.is_verified = True
        userOTP.save()
        return {"msg": "done"}

    def create(self, validated_data):
        return validated_data


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = New_User_Resgistration
        fields = ["id", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, data):
        if (
            len(data) < 8
            or not re.findall("\d", data)
            or not re.findall("[A-Z]", data)
            or not re.findall("[a-z]", data)
            or not re.findall("[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]", data)
        ):
            raise ValidationError(
                {
                    "msg": "The password needs to be more than 8 characters, contain atleast one uppercase,one lowercase and a special character"
                }
            )

        return data

    def validate_email(self, data):
        try:
            userOTP = OTP.objects.get(email=data)
        except:
            context = {"msg": "Please raise OTP for email verification"}
            raise ValidationError(context)
        if userOTP.is_verified == False:
            context = {"msg": "Please verify your email first"}
            raise ValidationError(context)
        return data

    def create(self, data):
        userOTP = OTP.objects.get(email=data["email"])
        user = New_User_Resgistration.objects.create(
            email=data["email"], password=data["password"]
        )
        user.password = make_password(data["password"])
        user.is_active = True
        user.save()
        userOTP.delete()
        return user


class LoginSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)
    email = serializers.EmailField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    tokens = serializers.JSONField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        try:
            user = New_User_Resgistration.objects.get(email__iexact=email)
        except:
            raise CustomValidation(
                detail="User is not registered with this Email Address",
                field="email",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        user = authenticate(email=email, password=password)
        if not user:
            raise CustomValidation(
                detail="Unable to authenticate with provided credentials",
                field="multiple",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return {
            "message": "Login Successful",
            "tokens": user.tokens,
        }

    def create(self, validated_data):
        return super().create(validated_data)
