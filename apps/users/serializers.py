from rest_framework import serializers
from .models import CustomUser


class SingUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'first_name', 'last_name']


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12)
    otp = serializers.CharField(max_length=6)

    class Meta:
        fields = ['phone_number', 'otp']


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12)

    class Meta:
        fields = ['phone_number']
