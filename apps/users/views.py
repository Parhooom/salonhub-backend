from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .serializers import SingUpUserSerializer, VerifyOTPSerializer, LoginSerializer
from .models import CustomUser
from .permissions import IsOwner

from random import randint
from django.core.cache import cache


@api_view(['POST'])
def signup(request):
    serializer = SingUpUserSerializer(data=request.data)

    if serializer.is_valid():
        phone_number = serializer.validated_data.get('phone_number')
        user = serializer.save()

        otp = randint(1000, 9999)
        cache.set(user.phone_number, otp, 120)
        print(f"OTP is {otp} for {phone_number}")

        return Response({"message": "Signup successful. Check console for OTP."})

    return Response(serializer.errors)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        phone_number = serializer.validated_data.get('phone_number')
        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if user is not None:
            otp = randint(1000, 9999)
            cache.set(user.phone_number, otp, 120)
            print(f"OTP is {otp} for {phone_number}")

            return Response({"message": "Login OTP sent. Check console for OTP."})

        else:
            return Response({"error": "User with this phone number does not exist."})

    return Response(serializer.errors)


@api_view(['POST'])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)

    if serializer.is_valid():
        phone_number = serializer.validated_data.get('phone_number')
        entered_otp = serializer.validated_data.get('otp')
        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if user is not None:
            otp = cache.get(phone_number)

            if otp is None:
                return Response({"error": "OTP has expired or does not exist."})

            if str(otp) == entered_otp:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})

            else:
                return Response({"error": "Invalid OTP."})

        else:
            return Response({"error": "User with this phone number does not exist."})
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    request.user.auth_token.delete()
    return Response("logged out", status=200)

