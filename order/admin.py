from django.contrib import admin
from .models import Order,ShippingOption,OrderItem
# Register your models here.
admin.site.register(Order)
admin.site.register(ShippingOption)
admin.site.register(OrderItem)
