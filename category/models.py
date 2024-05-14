from django.db import models
from django.urls import reverse

# Create your models here.

class ProductCategory(models.Model):
    catagory_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    catagory_image = models.ImageField(upload_to='images/catagories')

    def __str__(self):
        return self.catagory_name

class ShopCategory(models.Model):
    catagory_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    catagory_image = models.ImageField(upload_to='images/catagories')
    

    def __str__(self):
        return self.catagory_name