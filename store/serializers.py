from rest_framework import serializers
from.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'slug', 'image', 'stock', 'is_available', 'productHolder', 'category', 'price', 'description', 'created_at', 'modified_date']
