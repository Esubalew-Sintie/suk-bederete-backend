from rest_framework import serializers
from .models import Order, OrderItem, ShippingOption
from merchant.serializer import MerchantSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity_ordered']

class ShippingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingOption
        fields = ['name', 'cost', 'delivery_time']

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    merchant = MerchantSerializer()
    order_items = OrderItemSerializer(many=True)
    shipping_option = ShippingOptionSerializer()
    barcode_image = serializers.ImageField(required=False, use_url=True)  # Include barcode image

    class Meta:
        model = Order
        fields = ['unique_id', 'customer', 'merchant', 'total_amount', 'order_status', 'order_items', 'payment_status', 'payment_method', 'shipping_option', 'order_date', 'barcode_image']

    def get_customer(self, obj):
        return {
            'email': obj.customer.user.email,
            'first_name': obj.customer.first_name,
            'last_name': obj.customer.last_name,
            'address1': obj.customer.address1,
            'address2': obj.customer.address2,
            'zip_code': obj.customer.zip_code,
            'city': obj.customer.city,
            'state': obj.customer.state,
            'country': obj.customer.country,
            'phone_number': obj.customer.phone_number,
        }

    def get_merchant(self, obj):
        return {
            'email': obj.merchant.user.email,
        }

class OrderSerializerForMerchant(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    merchant = MerchantSerializer()
    order_items = OrderItemSerializer(many=True)
    shipping_option = ShippingOptionSerializer()
    # barcode_image = serializers.ImageField(required=False, use_url=True)  # Include barcode image

    class Meta:
        model = Order
        fields = [ 'customer', 'merchant', 'total_amount', 'order_status', 'order_items', 'payment_status', 'payment_method', 'shipping_option', 'order_date']

    def get_customer(self, obj):
        return {
            'email': obj.customer.user.email,
            'first_name': obj.customer.first_name,
            'last_name': obj.customer.last_name,
            'address1': obj.customer.address1,
            'address2': obj.customer.address2,
            'zip_code': obj.customer.zip_code,
            'city': obj.customer.city,
            'state': obj.customer.state,
            'country': obj.customer.country,
            'phone_number': obj.customer.phone_number,
        }

    def get_merchant(self, obj):
        return {
            'email': obj.merchant.user.email,
        }
