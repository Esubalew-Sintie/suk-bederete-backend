from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Template
from .serializer import TemplateSerializer
# Create your views here.
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status

@api_view(['GET'])
def getTemplates(request):
    templates = Template.objects.all()
    serializer = TemplateSerializer(instance=templates, many=True)
    return Response(serializer.data) 

@api_view(['GET'])
def getTemplate(request, pk):
    template = Template.objects.get(pk=pk)
    serializer = TemplateSerializer(instance=template, many=False)
    return Response(serializer.data)


class TemplateUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    lookup_field = 'pk'