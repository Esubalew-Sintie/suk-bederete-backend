from rest_framework import serializers
from.models import Order, ShippingOption, OrderItem
from product.serializers import ProductSerializer
from customer.serializer import CustomerSerializer
from merchant.serializer import MerchantSerializer
class ShippingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingOption
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity_ordered']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    merchant = MerchantSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    shipping_option = ShippingOptionSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id','customer', 'merchant', 'total_amount', 'order_status', 'order_items', 'payment_status', 'payment_method', 'shipping_option', 'order_date']
