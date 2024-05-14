from django.db import models
from merchant.models import Merchant

class Category(models.Model):
    name = models.CharField(max_length=200)

class Product(models.Model):
    productName = models.CharField(max_length=255)
    productDescription = models.TextField()
    quantity = models.IntegerField()
    productVariants = models.JSONField()
    productCategory = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='images/products/')  # Store images directly
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='products')
    inventory_limit = models.PositiveIntegerField(default=100)


    def __str__(self):
        return self.productName
