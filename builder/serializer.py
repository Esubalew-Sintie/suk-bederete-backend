from rest_framework.serializers import ModelSerializer
from .models import Template, Page, PageContent

class TemplateSerializer(ModelSerializer):
    class Meta:
        model= Template
        fields = '__all__' 

class PageSerializer(ModelSerializer):
    class Meta:
        model= Page
        fields = '__all__' 

class PageContentSerializer(ModelSerializer):
    class Meta:
        model= PageContent
        fields = '__all__' 