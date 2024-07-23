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
        role = request.data.get('role')
        print(role, email, password)

        if not email or not password or not role:
            print("Email, password, and role are required.")
            return Response({"error": "Email, password, and role are required."}, status=status.HTTP_400_BAD_REQUEST)

        if role not in [ 'client']:
            print("Invalid role. Role must be 'Customer' or 'client'.")
            return Response({"error": "Invalid role. Role must be client."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with the given email already exists
        user = Account.objects.filter(email=email).first()

        if not user:
            # Create the Account instance if the user does not exist
            user = Account.objects.create_user(email=email, password=password, role=role, is_active=True)
            print(user,role)
        else:
            # If the user already exists, ensure the role matches
            if user.role != role:
                print("User role mismatch")
                return Response({"error": "User role mismatch."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
                
        # Create the Customer instance with the extracted data
        if role == 'client':
            # Check if a Customer instance is already created
            if Customer.objects.filter(user=user).exists():
                return Response({"error": "Customer record already exists."}, status=status.HTTP_400_BAD_REQUEST)
            # Create the Customer instance
            customer = Customer.objects.create(user=user)
            # Serialize the Customer instance
            serializer = CustomerSerializer(customer, many=False)
            response_data = {
                'message': 'Customer registered successfully',
                'email': email,
                'tokens': tokens,
                'data': serializer.data,
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

            # Determine the role of the user and fetch the corresponding profile
            if user.role == 'client':
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


class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
class CustomerListView(APIView):
    def get(self, request, format=None):
        merchants = Customer.objects.all()
        serializer = CustomerSerializer(merchants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
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

