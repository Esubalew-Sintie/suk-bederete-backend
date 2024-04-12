from rest_framework.serializers import ModelSerializer
from .models import Shop, CustomizedPage

class ShopSerializer(ModelSerializer):
    class Meta:
        model= Shop
        fields = '__all__' 

class CustomizedPageSerializer(ModelSerializer):
    class Meta:
        model= CustomizedPage
        fields = '__all__' 