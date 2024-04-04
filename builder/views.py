from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Template, Page, PageContent
from .serializer import TemplateSerializer, PageContentSerializer, PageSerializer
from rest_framework import status
# Create your views here.
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status

@api_view(['GET'])
def getTemplates(request):
    templates = Template.objects.all()
    serializer = TemplateSerializer(instance=templates, many=True)
    return Response(serializer.data) 

@api_view(['GET'])
def getTemplatePages(request, template_id):
    try:
        # Retrieve the template object
        template = get_object_or_404(Template, pk=template_id)
        
        # Retrieve all pages associated with the template
        pages = Page.objects.filter(template=template)
        
        # Serialize the pages
        serializer = PageSerializer(pages, many=True)
        
        # Return the serialized data
        return Response(serializer.data)
    
    except Exception as e:
        # Handle exceptions
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def getTemplate(request, pk):
    template = Template.objects.get(pk=pk)
    serializer = TemplateSerializer(instance=template, many=False)
    return Response(serializer.data)

@api_view(['PATCH'])
def updatePageContent(request, pk):
    try:
        template = PageContent.objects.get(pk=pk)
        
        if 'content' in request.data:
            content = request.data['content']
            if 'html' in content:
                template.html = content['html']
            if 'css' in content:
                template.css = content['css']
        
        template.save()
        
        serializer = PageContentSerializer(template)
        return Response(serializer.data)
    
    except PageContent.DoesNotExist:
        return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
