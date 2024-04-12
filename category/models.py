from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    catagory_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    catagory_image = models.ImageField(upload_to='images/catagories')

    class Meta:
        verbose_name = 'catagory'
        verbose_name_plural = 'catagories'
    
    def get_url(self):
        return reverse('specific_product', args=[self.slug])

    def __str__(self):
        return self.catagory_name