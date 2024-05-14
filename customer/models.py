from django.db import models
from django.conf import settings

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField("Full name", max_length=1024)
    address1 = models.CharField("Address line 1", max_length=1024)
    address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
    zip_code = models.CharField("ZIP", max_length=12)
    city = models.CharField("City", max_length=1024)
    state = models.CharField("State", max_length=1024, blank=True, null=True)
    country = models.CharField("Country", max_length=1024)
    phone_number = models.CharField("Phone Number", max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
