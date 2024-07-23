from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from rest_framework.response import Response
from django.contrib.auth import authenticate
from account.serializer import AccountSerializer
from account.models import Account
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)
# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
# Create your views here.

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')

        if not email or not password or not role:
            print("Email, password, and role are required.")
            return Response({"error": "Email, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

        if role != 'merchant':
            print("Invalid role. Role must be 'merchant'.")
            return Response({"error": "Invalid role. Role must be 'merchant'."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with the given email already exists
        user = Account.objects.filter(email=email).first()

        if not user:
            # Create the Account instance if the user does not exist
            user = Account.objects.create_user(email=email, password=password, role=role, is_active=True)
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        user_data = AccountSerializer(user).data

        response_data = {
            'message': 'Admin registered successfully',
            'data': user_data,
            'tokens': tokens,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        
        print(password,email)
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password)
        if user:
            # Set the user as active
            user.is_active = True
            user.save()
            print(user,user.role)
            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            user_data = AccountSerializer(user).data

            response_data = {
                'message': 'Login successful',
                'tokens': tokens,
                "data":user_data
            }
            print(response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
