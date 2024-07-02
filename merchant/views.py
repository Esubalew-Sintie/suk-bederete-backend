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

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')

        if not email or not password or not role:
            return Response({"error": "Email, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

        if role not in ['merchant', 'client']:
            return Response({"error": "Invalid role. Role must be 'merchant' or 'client'."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Account instance
        user = Account.objects.create_user(email=email, password=password, role=role, is_active=True)

        if role == 'merchant':
            # Create the Merchant instance
            merchant = Merchant.objects.create(user=user, bank_account_number="")
            # Serialize the merchant instance
            serializer = MerchantSerializer(merchant, many=False)
        else:
            # Create the Client instance
            client = Customer.objects.create(user=user)
            # Serialize the client instance
            serializer = CustomerSerializer(client, many=False)

        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        response_data = {
            'message': f'{role.capitalize()} registered successfully',
            'email': email,
            'tokens': tokens,
            role: serializer.data,  # Include the serialized profile data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
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
