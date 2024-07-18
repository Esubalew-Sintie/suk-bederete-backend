from django.db import models
from django.conf import settings
import uuid


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField("First name", max_length=1024,blank=True, null=True)
    last_name = models.CharField("Last name", max_length=1024,blank=True, null=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True) 
    address1 = models.CharField("Address line 1", max_length=1024,blank=True, null=True)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField("ZIP", max_length=12,blank=True, null=True)
    city = models.CharField("City", max_length=1024,blank=True, null=True)
    state = models.CharField("State", max_length=1024, blank=True, null=True)
    country = models.CharField("Country", max_length=1024,blank=True, null=True)
    phone_number = models.CharField("Phone Number", max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
