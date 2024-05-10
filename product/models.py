from django.db import models

class Product(models.Model):
    productName = models.CharField(max_length=255)
    productDescription = models.TextField()
    quantity = models.IntegerField()
    productVariants = models.JSONField()
    productCategory = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='images/products/')  # Store images directly

    def __str__(self):
        return self.productName
