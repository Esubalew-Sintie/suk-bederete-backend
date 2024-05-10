from django.db import models
from merchant.models import Merchant
from builder.models import Template, Page
from account.models import Account
from django.apps import apps
import uuid
# Create your models here.
class CustomizedTemplate(models.Model):
    original_template = models.ForeignKey(Template, on_delete=models.CASCADE)
    modifiedby = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='customized_templates', to_field='unique_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_template.name
    
class CustomizedPage(models.Model):
    customized_template = models.ForeignKey(CustomizedTemplate, related_name='pages', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()

    def __str__(self):
        return f"{self.customized_template.original_template.name} - {self.name}"

class Shop(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Merchant, on_delete=models.CASCADE, to_field='unique_id')
    customized_template = models.ForeignKey(CustomizedTemplate, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Unique identifier for the shop
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ShopRating(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.IntegerField()  # You can define your rating system here
    comment = models.TextField(blank=True, null=True)  # Optional comment from the user

    def __str__(self):
        return f"{self.shop.name} - {self.user.username} - {self.rating}"