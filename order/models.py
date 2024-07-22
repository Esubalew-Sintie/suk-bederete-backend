from django.conf import settings
from django.db import models
from django.utils import timezone
from merchant.models import Merchant
from store.models import Product  # Corrected to match the model name
from customer.models import Customer  # Corrected to match the model name
import uuid

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(Customer, to_field='unique_id', on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='Pending',  # This should match one of the values in the choices
    )
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True) 
    order_items = models.ManyToManyField('OrderItem', related_name='orders')
    payment_status = models.CharField(max_length=40)
    barcode_image = models.ImageField(upload_to="images/bar-code/", blank=True, null=True)
    payment_method = models.CharField(max_length=50)
    shipping_option = models.ForeignKey('ShippingOption', on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(default=timezone.now)

    def calculate_total_cost(self):
        return sum(item.product.price * item.quantity_ordered for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} by {self.customer.user.email} for {self.merchant.user.email}"


class ShippingOption(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_time = models.DurationField()

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Changed to ForeignKey
    quantity_ordered = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_ordered}"
