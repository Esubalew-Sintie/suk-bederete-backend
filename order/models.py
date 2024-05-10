from django.db import models
from django.utils import timezone

class Order(models.Model):
    product = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    paymentStatus = models.CharField(max_length=20)
    payment = models.CharField(max_length=50)
    shippingMethod = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    placedBy = models.CharField(max_length=50)
    action = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product} - {self.placedBy}"

    class Meta:
        ordering = ['-date']  # Orders will be displayed newest first
