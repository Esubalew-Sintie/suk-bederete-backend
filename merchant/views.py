from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from rest_framework.response import Response
from django.contrib.auth import authenticate
from.serializer import MerchantSerializer
from.models import Merchant
from account.serializer import AccountSerializer
from account.models import Account
from rest_framework_simplejwt.tokens import RefreshToken
from customer.models import Customer
from customer.serializer import CustomerSerializer
import logging

logger = logging.getLogger(__name__)
# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Merchant

class CustomerUpdateView(APIView):
    def patch(self, request, unique_id, format=None):
        serializer = None
        print("Request data:", request.data)
        uid = request.data.get('uid', None)
        print("UID:", uid)

        try:
            if uid:
                user = Account.objects.get(pk=uid)
                print("User found:", user)
               
                try:
                    # Check if a Merchant instance already exists for the user
                    customer = Customer.objects.get(user=user)
                    print("Customer found:", customer)
                    # Update the existing customer instance
                    serializer = CustomerSerializer(customer, data=request.data, partial=True)
                    print("Serializer initialized for existing customer")
                except Customer.DoesNotExist:
                    # Create a new Merchant instance
                    print("customer does not exist, creating a new one")
                    customer = Customer(user=user)
                    serializer = CustomerSerializer(customer, data=request.data, partial=True)
                    print("Serializer initialized for new customer")
        except Account.DoesNotExist:
            print("User not found")
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if serializer:
            print("Serializer before validation:", serializer)
            if serializer.is_valid():
                print("Serializer is valid")
                serializer.save()
                print("customer data saved")
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print("Serializer errors:", serializer.errors)
                # Return detailed errors in case of validation failure
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Serializer not initialized")
            return Response({"detail": "Serializer not initialized."}, status=status.HTTP_400_BAD_REQUEST)
        
        
class MerchantUpdateView(APIView):
    def patch(self, request, unique_id, format=None):
        serializer = None
        print("Request data:", request.data)
        try:
            # Check if a Merchant instance already exists for the user
            merchant = Merchant.objects.get(unique_id=unique_id)
            print("Merchant found:", merchant)
            # Update the existing Merchant instance
            serializer = MerchantSerializer(merchant, data=request.data, partial=True)
            print("Serializer initialized for existing merchant")
        except Merchant.DoesNotExist:
            # Create a new Merchant instance
            print("Merchant does not exist, creating a new one")
            merchant = Merchant(unique_id=unique_id)
            serializer = MerchantSerializer(merchant, data=request.data, partial=True)
            print("Serializer initialized for new merchant")

            

        if serializer:
            print("Serializer before validation:", serializer)
            if serializer.is_valid():
                print("Serializer is valid")
                serializer.save()
                print("Merchant data saved")
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print("Serializer errors:", serializer.errors)
                # Return detailed errors in case of validation failure
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Serializer not initialized")
            return Response({"detail": "Serializer not initialized."}, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
        print(role, email, password)

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
        else:
            # If the user already exists, ensure the role matches
            if user.role != role:
                return Response({"error": "User role mismatch."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # Check if a Merchant instance is already created
        if Merchant.objects.filter(user=user).exists():
            return Response({"error": "Merchant record already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Merchant instance
        merchant = Merchant.objects.create(user=user)
        # Serialize the merchant instance
        serializer = MerchantSerializer(merchant, many=False)
        response_data = {
            'message': 'Merchant registered successfully',
            'email': email,
            'tokens': tokens,
            'merchant': serializer.data,
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
            
            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            # Determine the role of the user and fetch the corresponding profile
            if user.role == 'merchant':
                profile = Merchant.objects.get(user=user)
                profile_serializer = MerchantSerializer(profile, many=False)
            else:
                profile = Customer.objects.get(user=user)
                profile_serializer = CustomerSerializer(profile, many=False)

            response_data = {
                'message': 'Login successful',
                'data': profile_serializer.data,
                'tokens': tokens,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
