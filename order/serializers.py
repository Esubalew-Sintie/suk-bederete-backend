from rest_framework import serializers
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from .models import Order, OrderItem, ShippingOption
from merchant.models import Merchant
from customer.models import Customer
from store.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity_ordered']

class ShippingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingOption
        fields = ['id', 'name', 'cost', 'delivery_time']

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    merchant = serializers.PrimaryKeyRelatedField(queryset=Merchant.objects.all())
    order_items = OrderItemSerializer(many=True)
    shipping_option = serializers.PrimaryKeyRelatedField(queryset=ShippingOption.objects.all(), allow_null=True)
    barcode_image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = Order
        fields = [
            'unique_id', 'customer', 'merchant', 'total_amount', 'order_status',
            'payment_status', 'payment_method', 'shipping_option', 'order_items',
            'order_date', 'barcode_image'
        ]

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        shipping_option = validated_data.pop('shipping_option', None)
        
        # Create Order instance
        order = Order.objects.create(**validated_data, shipping_option=shipping_option)
        
        # Create OrderItem instances and associate them with the Order
        order_items = []
        for item_data in order_items_data:
            product_id = item_data['product'].id
            product = Product.objects.get(id=product_id)
            order_item = OrderItem.objects.create(product=product, quantity_ordered=item_data['quantity_ordered'])
            order_items.append(order_item)
        
        # Associate OrderItem instances with the Order
        order.order_items.set(order_items)
        
        # Generate and save the barcode image
        self.generate_barcode(order)
        
        return order

    def generate_barcode(self, order):
        unique_id = str(order.unique_id)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(unique_id)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Save QR code to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Save the image to the barcode_image field
        order.barcode_image.save(f'{unique_id}.png', ContentFile(buffer.getvalue()), save=True)
