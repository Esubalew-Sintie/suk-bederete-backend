from django.db import models
from account.models import Account
# Create your models here.
class Merchant(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    bank_account_number = models.CharField(max_length=20)
    has_physical_store = models.BooleanField(default=False)
    physical_shop_name = models.CharField(max_length=200, blank=True, null=True)
    physical_shop_address = models.TextField(blank=True, null=True)
    physical_shop_city = models.CharField(max_length=100, blank=True, null=True)
    physical_shop_phone_number = models.CharField(max_length=15, blank=True, null=True)
    online_shop_type = models.CharField(max_length=100, choices=[
        ('electronics', 'Electronics Shop'),
        ('household', 'Household Shop'),
        ('clothing', 'Clothing Shop'),
        # Add other options as needed
    ], blank=True, null=True)

    def __str__(self):
        return self.user.email