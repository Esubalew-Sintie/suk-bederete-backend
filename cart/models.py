from django.db import models
from store.models import Product
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    dated_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class Cart_item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        sub_total = self.product.price * self.quantity
        return sub_total

    def __str__(self):
        return self.product