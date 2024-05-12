from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from.serializer import MerchantSerializer
from.models import Merchant
from account.serializer import AccountSerializer
from account.models import Account
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the Account instance
        user = Account.objects.create_user(email=email, password=password, is_active=True)
        
        # Create the Merchant instance with minimal information
        merchant = Merchant.objects.create(user=user, bank_account_number="")
        
        # Serialize the merchant instance
        serializer = MerchantSerializer(merchant, many=False)

        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        response_data = {
            'message': 'Merchant registered successfully',
            'email': email,
            'tokens': tokens,
            'merchant': serializer.data,  # Include the serialized merchant data
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
            # Set the merchant as active
            user.is_active = True
            user.save()
            
            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            # Include the merchant's unique_id in the response
            merchant = Merchant.objects.get(user=user)
            merchant_serializer = MerchantSerializer(merchant, many=False)
            merchant_data = merchant_serializer.data
            merchant_data['unique_id'] = merchant.unique_id  # Add the unique_id to the merchant data
            
            response_data = {
                'message': 'Login successful',
                'merchant': merchant_data,
                'tokens': tokens,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
