from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Template, Page
from .serializer import TemplateSerializer, PageSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import status
# Create your views here.
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getTemplates(request):
    templates = Template.objects.all()
    serializer = TemplateSerializer(instance=templates, many=True)
    return Response(serializer.data) 

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getTemplate(request, pk):
    template = Template.objects.get(pk=pk)
    serializer = TemplateSerializer(instance=template, many=False)
    return Response(serializer.data)

@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updatePageContent(request, template_id, page_id):
    try:
        # Get the specific page related to the template_id and page_id
        page = Page.objects.get(template_id=template_id, pk=page_id)
        
        if 'content' in request.data:
            content = request.data['content']
            if 'html' in content:
                page.html = content['html']
            if 'css' in content:
                page.css = content['css']
            if 'js' in content:
                page.js = content['js']
        
        page.save()
        
        # You may customize the serializer according to your needs
        serializer = PageSerializer(page)
        return Response(serializer.data)
        
        return Response({"success": "Page content updated successfully"})
    
    except Page.DoesNotExist:
        return Response({"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getePage(request, template_id, page_id):
    try:
        # Get the specific page related to the template_id and page_id
        page = Page.objects.get(template_id=template_id, pk=page_id)
        
        # You may customize the serializer according to your needs
        serializer = PageSerializer(page)
        return Response(serializer.data)
        
        return Response({"success": "Page content updated successfully"})
    
    except Page.DoesNotExist:
        return Response({"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getTemplatePage(request, template_id):
    try:
        # Retrieve the template object
        template = get_object_or_404(Template, pk=template_id)
        
        # Retrieve all pages associated with the template
        page = Page.objects.filter(template=template)
    
        serializer = PageSerializer(instance=page, many=True)
        
        
        # Return the serialized data for all pages
        return Response(serializer.data)
    
    except Exception as e:
        # Handle exceptions
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
