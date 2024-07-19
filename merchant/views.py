from rest_framework import status
from rest_framework.decorators import api_view
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

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')

        if not email or not password or not role:
            return Response({"error": "Email, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

        if role not in ['merchant', 'customer']:
            return Response({"error": "Invalid role. Role must be 'merchant' or 'customer'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the Account instance
            user = Account.objects.create_user(email=email, password=password, role=role, is_active=True)
            logger.debug(f"Created user: {user.email}")

            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            if role == 'merchant':
                # Fetch the Merchant instance created by the signal
                merchant = Merchant.objects.get(user=user)
                serializer = MerchantSerializer(merchant, many=False)
                response_data = {
                    'message': 'Merchant registered successfully',
                    'email': email,
                    'tokens': tokens,
                    'merchant': serializer.data,
                }
            else:
                # Fetch the Customer instance created by the signal
                customer = Customer.objects.get(user=user)
                serializer = CustomerSerializer(customer, many=False)
                response_data = {
                    'message': 'Customer registered successfully',
                    'email': email,
                    'tokens': tokens,
                    'customer': serializer.data,
                }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
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
                'profile': profile_serializer.data,
                'tokens': tokens,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
