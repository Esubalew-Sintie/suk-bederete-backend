import json
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.http import StreamingHttpResponse
# views.py
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import json
import qrcode
# from .serializers import OrderSerializerForMerchant
from rest_framework import generics

from io import BytesIO
from rest_framework import status

from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import  CreateAPIView
from.models import Order  
from merchant.models import Merchant 
from customer.models import Customer  
 
from.serializers import OrderSerializer

# class OrderUpdateDestroyView(UpdateAPIView, DestroyAPIView, ListModelMixin):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from io import BytesIO
import qrcode
from .models import Order
from .serializers import OrderSerializer

    

class OrderCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
# class OrderCreateView(CreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def perform_create(self, serializer):
#         order = serializer.save()

#         # Generate QR code
        # unique_id = str(order.unique_id)
        # qr = qrcode.QRCode(
        #     version=1,
        #     error_correction=qrcode.constants.ERROR_CORRECT_L,
        #     box_size=10,
        #     border=4,
        # )
        # qr.add_data(unique_id)
        # qr.make(fit=True)
        # img = qr.make_image(fill='black', back_color='white')

        # # Save QR code to a BytesIO object
        # buffer = BytesIO()
        # img.save(buffer, format='PNG')
        # buffer.seek(0)

        # # Save the image to the barcode_image field
        # order.barcode_image.save(f'{unique_id}.png', ContentFile(buffer.getvalue()), save=False)
        # order.save()

#         # Send UUID to customer via email
#         # send_mail(
#         #     'Your Order UUID',
#         #     f'Your order UUID is {unique_id}. Please use this for tracking your order.',
#         #     'from@example.com',  # Replace with your email
#         #     [order.customer.user.email],
#         #     fail_silently=False,
#         # )

#         # Prepare order information to send to merchant (excluding UUID and barcode image)
#         order_info = {
#             'customer': {
#                 'email': order.customer.user.email,
#                 'first_name': order.customer.first_name,
#                 'last_name': order.customer.last_name,
#                 'address1': order.customer.address1,
#                 'address2': order.customer.address2,
#                 'zip_code': order.customer.zip_code,
#                 'city': order.customer.city,
#                 'state': order.customer.state,
#                 'country': order.customer.country,
#                 'phone_number': order.customer.phone_number,
#             },
#             'total_amount': order.total_amount,
#             'order_status': order.order_status,
#             "barcode_image": order.barcode_image,
#             'order_items': [{'product': item.product.name, 'quantity': item.quantity_ordered} for item in order.order_items.all()],
#             'payment_status': order.payment_status,
#             'payment_method': order.payment_method,
#             'shipping_option': {
#                 'name': order.shipping_option.name,
#                 'cost': order.shipping_option.cost,
#                 'delivery_time': order.shipping_option.delivery_time.seconds // 60,
#             } if order.shipping_option else None,
#             'order_date': order.order_date.isoformat(),
#         }

#         # Send order information to merchant via email
#         # send_mail(
#         #     'New Order Received',
#         #     json.dumps(order_info, indent=2),
#         #     'from@example.com',  # Replace with your email
#         #     [order.merchant.user.email],
#         #     fail_silently=False,
#         # )

#         return Response(order_info, status=status.HTTP_201_CREATED)

class CustomerOrdersView(APIView):
    def get(self, request, customer_id, format=None):
        try:
            # Retrieve the customer based on the unique ID
            customer = Customer.objects.get(unique_id=customer_id)
            
            # Filter orders by the customer
            orders = Order.objects.filter(customer=customer)
            
            # Serialize the orders
            serializer = OrderSerializer(orders, many=True)
            
            order_infos = serializer.data


            return Response(order_infos)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)




class MerchantOrdersView(APIView):
    def get(self, request, merchant_id, format=None):
        try:
            # Retrieve the merchant based on the unique ID
            merchant = Merchant.objects.get(unique_id=merchant_id)
            
            # Filter orders by the merchant
            orders = Order.objects.filter(merchant=merchant)
            
            # Serialize the orders using the merchant-facing serializer
            serializer = OrderSerializerForMerchant(orders, many=True)
            
            order_infos = serializer.data

            return Response(order_infos)
        except Merchant.DoesNotExist:
            return Response({"error": "Merchant not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


def compare_with_previous_state(current_orders, initial_data):
    new_or_updated_orders = []
    initial_data_dict = {order.unique_id: order for order in initial_data}
    
    for order in current_orders:
        if order.unique_id not in initial_data_dict:
            new_or_updated_orders.append(order)
        else:
            existing_order = initial_data_dict[order.unique_id]
            if (order.total_amount != existing_order.total_amount or 
                order.order_status != existing_order.order_status or 
                order.payment_status != existing_order.payment_status):
                new_or_updated_orders.append(order)
                
    return new_or_updated_orders

def event_stream(merchant_id):
    initial_data = list(Order.objects.filter(merchant=merchant_id).order_by("-order_date"))

    while True:
        current_orders = list(Order.objects.filter(merchant=merchant_id).order_by("-order_date"))
        new_or_updated_orders = compare_with_previous_state(current_orders, initial_data)
        initial_data = current_orders

        if new_or_updated_orders:
            data = json.dumps([{
                'customer': {
                    'email': order.customer.user.email,
                    'first_name': order.customer.first_name,
                    'last_name': order.customer.last_name,
                    'address1': order.customer.address1,
                    'address2': order.customer.address2,
                    'zip_code': order.customer.zip_code,
                    'city': order.customer.city,
                    'state': order.customer.state,
                    'country': order.customer.country,
                    'phone_number': order.customer.phone_number,
                },
                'total_amount': str(order.total_amount),  # Ensure total_amount is string
                'order_status': order.order_status,
                'order_items': [{'product': item.product.name, 'quantity': item.quantity_ordered} for item in order.order_items.all()],
                'payment_status': order.payment_status,
                'payment_method': order.payment_method,
                'shipping_option': {
                    'name': order.shipping_option.name if order.shipping_option else None,
                    'cost': str(order.shipping_option.cost) if order.shipping_option else None,
                    'delivery_time': order.shipping_option.delivery_time.total_seconds() // 60 if order.shipping_option else None,
                },
                'order_date': order.order_date.isoformat(),
            } for order in new_or_updated_orders], cls=DjangoJSONEncoder)
            yield f"data: {data}\n\n"

        time.sleep(1)




class OrderStreamView(View):
    def get(self, request, merchant_id):
        merchant = get_object_or_404(Merchant, unique_id=merchant_id)
        response = StreamingHttpResponse(event_stream(merchant.unique_id))
        response['Content-Type'] = 'text/event-stream'
        return response


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer