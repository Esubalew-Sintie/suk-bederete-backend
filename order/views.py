import json
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.http import StreamingHttpResponse
from django.views import View
from rest_framework.views import APIView
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
    for order in current_orders:
        # Check if the order is new
        if not initial_data:  # Handle the case where initial_data is empty
            new_or_updated_orders.append(order)
        elif order.id not in [o.id for o in initial_data]:
            new_or_updated_orders.append(order)
        else:
            # Check if the order is updated
            existing_order = next((o for o in initial_data if o.id == order.id), None)
            if existing_order:
                # Compare fields to determine if the order is updated
                if order.total_amount!= existing_order.total_amount or order.order_status!= existing_order.order_status or order.payment_status!= existing_order.payment_status:
                    new_or_updated_orders.append(order)
    return new_or_updated_orders

def event_stream(merchant_id):
    # Initialize initial_data as an empty list
    initial_data = Order.objects.filter(merchant_id=merchant_id).order_by("-id")
    
    while True:
        # Fetch the current state of orders
        current_orders = Order.objects.filter(merchant_id=merchant_id).order_by("-id")
        
        # Compare with the previous state to find new or updated orders
        new_or_updated_orders = compare_with_previous_state(current_orders, initial_data)
        
        # Update the initial data with the new or updated orders
        initial_data = current_orders
        
        # Convert the orders to JSON and yield
        if new_or_updated_orders:
            data = json.dumps([{
                'id': order.id,
                'customer': order.customer.user.email,
                'merchant': order.merchant.user.email,
                'total_amount': order.total_amount,
                'order_status': order.order_status,
                'order_items': [{'product': item.product.productName, 'quantity': item.quantity_ordered} for item in order.order_items.all()],
                'payment_status': order.payment_status,
                'payment_method': order.payment_method,
                'shipping_option': {'name': order.shipping_option.name,'cost': order.shipping_option.cost,'delivery_time': order.shipping_option.delivery_time.seconds // 60,},                
                'order_date': order.order_date.isoformat(),
            } for order in new_or_updated_orders], cls=DjangoJSONEncoder)
            yield "\ndata: {}\n\n".format(data)
            
            # Sleep for a short period to avoid overwhelming the client
        time.sleep(1)

class OrderStreamView(View):
    def get(self, request, merchant_id):
        response = StreamingHttpResponse(event_stream(merchant_id))
        response['Content-Type'] = 'text/event-stream'
        return response
