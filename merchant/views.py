from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializer import MerchantSerializer
from .models import Merchant
from account.serializer import AccountSerializer
from account.models import Account
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a random password
        password = Account.objects.make_random_password()
        
        # Create the Account instance
        user = Account.objects.create_user(email=email, password=password)
        
        # Create the Merchant instance with minimal information
        merchant = Merchant.objects.create(user=user, bank_account_number="")

        serializer = MerchantSerializer(merchant, many=False)

        return Response(serializer.data)
        
        return Response({"message": "Merchant registered successfully", "email": email}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        account = authenticate(request, email=email, password=password)
        if account is not None:
            # You can return a token or session here
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)