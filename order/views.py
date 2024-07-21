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

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import  CreateAPIView
from.models import Order  
from merchant.models import Merchant  
from.serializers import OrderSerializer

class OrderUpdateDestroyView(UpdateAPIView, DestroyAPIView, ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MerchantOrdersView(APIView):
    def get(self, request, merchant_id, format=None):
        try:
            # Attempt to retrieve the merchant based on the unique ID
            merchant = Merchant.objects.get(unique_id=merchant_id)
            
            # Validate the merchant exists
            if not merchant:
                raise serializers.ValidationError("Merchant not found.")
            
            # Filter orders by the merchant
            orders = Order.objects.filter(merchant=merchant)
            
            # Serialize the orders
            serializer = OrderSerializer(orders, many=True)
            
            return Response(serializer.data)
        except serializers.ValidationError as e:
            # Handle validation errors
            return Response({"error": str(e)}, status=400)

class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

def compare_with_previous_state(current_orders, initial_data):
    new_or_updated_orders = []
    initial_data_dict = {order.id: order for order in initial_data}
    
    for order in current_orders:
        if order.id not in initial_data_dict:
            new_or_updated_orders.append(order)
        else:
            existing_order = initial_data_dict[order.id]
            if (order.total_amount != existing_order.total_amount or 
                order.order_status != existing_order.order_status or 
                order.payment_status != existing_order.payment_status):
                new_or_updated_orders.append(order)
                
    return new_or_updated_orders

def event_stream(merchant_id):
    initial_data = list(Order.objects.filter(merchant_id=merchant_id).order_by("-id"))
    
    while True:
        current_orders = list(Order.objects.filter(merchant_id=merchant_id).order_by("-id"))
        new_or_updated_orders = compare_with_previous_state(current_orders, initial_data)
        initial_data = current_orders
        
        if new_or_updated_orders:
            data = json.dumps([{
                'id': order.id,
                'customer': order.customer.user.email,
                'merchant': order.merchant.user.email,
                'total_amount': order.total_amount,
                'order_status': order.order_status,
                'order_items': [{'product': item.product.name, 'quantity': item.quantity_ordered} for item in order.order_items.all()],
                'payment_status': order.payment_status,
                'payment_method': order.payment_method,
                'shipping_option': {'name': order.shipping_option.name,'cost': order.shipping_option.cost,'delivery_time': order.shipping_option.delivery_time.seconds // 60,},                
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

