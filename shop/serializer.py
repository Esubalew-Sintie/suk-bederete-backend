from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from.models import Picture

from .models import Shop, CustomizedPage, CustomizedTemplate
from django import forms
# serializers.py
from.models import Screenshot
class ShopSerializer(ModelSerializer):
    class Meta:
        model= Shop
        fields = '__all__' 

class CustomizedTemplateSerializer(ModelSerializer):
    class Meta:
        model= CustomizedTemplate
        fields = '__all__'

class CustomizedPageSerializer(ModelSerializer):
    class Meta:
        model= CustomizedPage
        fields = '__all__'



class ScreenshotCreateSerializer(ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ['image']




class PictureUploadSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        allow_empty=False  # Ensures that the list cannot be empty
    )

    def create(self, validated_data):
        files = validated_data.get('files', [])
        for file in files:
            picture = Picture(image=file)
            picture.save()
        return files