from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Shop, CustomizedTemplate, CustomizedPage
from .serializer import ShopSerializer, CustomizedPageSerializer, CustomizedTemplateSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from builder.models import Template
from django.shortcuts import get_object_or_404
from merchant.models import Merchant
import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def save_customized_pages(request):
    try:
        if request.method == 'POST':
            # Use the CustomizedTemplateSerializer to validate the input data
            serializer = CustomizedTemplateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            template = serializer.validated_data.get('original_template')
            modifier = serializer.validated_data.get('modifiedby')
            modified_pages_data = request.data.get('modified_pages', {})

            print(f"Received request: template={template}, modified_pages={modified_pages_data}")

            if not template:
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    customized_template = CustomizedTemplate.objects.create(original_template=template, modifiedby=modifier)
                    customized_template.save()

                    # Process modified pages
                    for page_name, page_data in modified_pages_data.items():
                        html = page_data.get('html')
                        css = page_data.get('css')
                        js = page_data.get('js', '') # Assuming JS is optional

                        print(f"Processing page: {page_name}, html={html}, css={css}, js={js}")

                        if html and css:
                            # Update or create a new customized page instance
                            CustomizedPage.objects.update_or_create(
                                customized_template=customized_template,
                                name=page_name,
                                defaults={'html': html, 'css': css, 'js': js}
                            )
            except ObjectDoesNotExist:
                return Response({"error": "Template or Customized template not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Customized pages saved successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("Error saving customized pages: %s", e)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PATCH'])
def update_customized_template(request, template_id):
    try:
        if request.method == 'PATCH':
            modified_pages_data = request.data.get('modified_pages', {})

            print(f"Received request: template_id={template_id}, modified_pages={modified_pages_data}")

            try:
                customized_template = CustomizedTemplate.objects.get(id=template_id)
                
                with transaction.atomic():
                    

                    # Process modified pages
                    for page_name, page_data in modified_pages_data.items():
                        html = page_data.get('html')
                        css = page_data.get('css')
                        js = page_data.get('js', '') # Assuming JS is optional

                        if html and css:
                            # Update or create a new customized page instance
                            CustomizedPage.objects.update_or_create(
                                customized_template=customized_template,
                                name=page_name,
                                defaults={'html': html, 'css': css, 'js': js}
                            )

            except ObjectDoesNotExist:
                return Response({"error": "Customized template not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Customized template updated successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("Error updating customized template: %s", e)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_customizedTemplate(request, merchant_id):
    logger.info(f"Received request for CustomizedTemplate modified by Merchant with ID: {merchant_id}")
    try:
        customised_Template = CustomizedTemplate.objects.get(modifiedby__unique_id=merchant_id)
    except CustomizedTemplate.DoesNotExist:
        logger.error(f"No CustomizedTemplate found modified by Merchant with ID: {merchant_id}")
        return Response({"error": "No CustomizedTemplate found modified by the given Merchant ID"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomizedTemplateSerializer(customised_Template, many=False)
    return Response(serializer.data)

#create shop
@api_view(['POST'])
def create_shop(request):
    if request.method == 'POST':
        name = request.data.get('name')
        template_id = request.data.get('template')
        if not name or not template_id:
            return Response({"error": "Name and template are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        owner = request.user.merchant
        template = get_object_or_404(Template, id=template_id)
        customized_template = CustomizedTemplate.objects.create(original_template=template, modifiedby=owner)
        customized_template.save()
        
        shop = Shop.objects.create(name=name, owner=owner, customized_template=customized_template)
        shop.save()
        
        serializer = ShopSerializer(shop, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#create a view to get a single page with the given template_id and page_id
@api_view(['GET'])
def get_customizedPage(request, template_id, page_name):
    try:
        customized_page = CustomizedPage.objects.get(customized_template=template_id, name=page_name)
    except CustomizedPage.DoesNotExist:
        return Response({"error": "Customized Page not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CustomizedPageSerializer(customized_page, many=False)
    return Response(serializer.data)