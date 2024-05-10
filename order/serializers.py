from rest_framework import serializers
from.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'product', 'status', 'paymentStatus', 'payment', 'shippingMethod', 
            'amount', 'date', 'placedBy', 'action'
        ]
