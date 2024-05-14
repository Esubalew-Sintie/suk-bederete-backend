from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from.models import Customer
from account.models import Account
from.serializer import CustomerSerializer
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
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
        
        # Extract data from the request
        name = request.data.get('name', "")
        address1 = request.data.get('address1', "")
        address2 = request.data.get('address2', "")
        zip_code = request.data.get('zip_code', "")
        city = request.data.get('city', "")
        state = request.data.get('state', "")
        country = request.data.get('country', "")
        phone_number = request.data.get('phone_number', "")
        
        # Create the Customer instance with the extracted data
        customer = Customer.objects.create(
            user=user,
            name=name,
            address1=address1,
            address2=address2,
            zip_code=zip_code,
            city=city,
            state=state,
            country=country,
            phone_number=phone_number
        )
        
        # Serialize the customer instance
        serializer = CustomerSerializer(customer, many=False)

        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        response_data = {
            'message': 'Customer registered successfully',
            'email': email,
            'tokens': tokens,
            'customer': serializer.data,  # Include the serialized customer data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

# views.py (continued)
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password)
        if user:
            # Set the customer as active
            user.is_active = True
            user.save()
            
            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            # Include the customer's information in the response
            customer = Customer.objects.get(user=user)
            customer_serializer = CustomerSerializer(customer, many=False)
            customer_data = customer_serializer.data
            
            response_data = {
                'message': 'Login successful',
                'customer': customer_data,
                'tokens': tokens,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)


class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    
class CustomerDetail(APIView):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
   
    
class CustomerUpdate(APIView):
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDelete(APIView):
    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerCreate(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

