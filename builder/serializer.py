from rest_framework.serializers import ModelSerializer
from .models import Template, Page

class TemplateSerializer(ModelSerializer):
    class Meta:
        model= Template
        fields = '__all__' 

class PageSerializer(ModelSerializer):
    class Meta:
        model= Page
        fields = '__all__' 

