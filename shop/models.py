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
    preview_image = models.ImageField(upload_to="images/preview/", blank=True, null=True)
    customized_template = models.ForeignKey(CustomizedTemplate, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=255, unique=True, blank=True, editable=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.unique_id:
            # Generate the custom unique ID
            new_uuid = uuid.uuid4()
            potential_unique_id = f"{self.name}-{new_uuid}"

            # Ensure the custom ID is unique
            while Shop.objects.filter(unique_id=potential_unique_id).exists():
                new_uuid = uuid.uuid4()
                potential_unique_id = f"{self.name}-{new_uuid}"
            
            self.unique_id = potential_unique_id
        
        super().save(*args, **kwargs)
    
class ShopRating(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.IntegerField()  # You can define your rating system here
    comment = models.TextField(blank=True, null=True)  # Optional comment from the user
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shop.name} - {self.user.email} - {self.rating}"
   
   
class Screenshot(models.Model):
    image = models.ImageField(upload_to='images/screenshots/')
    caption = models.CharField(max_length=255, blank=True)


class Picture(models.Model):
    image = models.ImageField(upload_to='pictures/')
