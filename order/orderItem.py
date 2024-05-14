# from django.db import models
# from product.models import Product  # Import the Product model
# from .models import Order  # Import the Product model

# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     quantity_ordered = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.product.name} - {self.quantity_ordered}"
