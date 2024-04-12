from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Shop, CustomizedTemplate, CustomizedPage
from .serializer import ShopSerializer, CustomizedPageSerializer
import logging
from builder.models import Template
from django.shortcuts import get_object_or_404
logger = logging.getLogger(__name__)

@api_view(['POST'])
def save_customized_pages(request):
    try:
        if request.method == 'POST':
            # Adjusted to match the payload key
            template_id = request.data.get('template')
            modified_pages_data = request.data.get('modified_pages', {})

            print(f"Received request: template_id={template_id}, modified_pages={modified_pages_data}")

            if not template_id:
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                original_template = Template.objects.get(id=template_id)
                customized_template = CustomizedTemplate.objects.create(original_template=original_template)
                customized_template.save()
            except CustomizedTemplate.DoesNotExist:
                return Response({"error": "Customized template not found"}, status=status.HTTP_404_NOT_FOUND)

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

            return Response({"message": "Customized pages saved successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("Error saving customized pages: %s", e)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_customizedTemplate(request, customised_TemplateId):
    logger.info(f"Received request for CustomizedTemplate with ID: {customised_TemplateId}")
    try:
        customised_Template = CustomizedTemplate.objects.get(id=customised_TemplateId)
    except CustomizedTemplate.DoesNotExist:
        logger.error(f"No CustomizedTemplate found with ID: {customised_TemplateId}")
        return Response({"error": "No CustomizedTemplate found with the given ID"}, status=status.HTTP_404_NOT_FOUND)

    customised_pages = CustomizedPage.objects.filter(customized_template=customised_Template)
    serializer = CustomizedPageSerializer(customised_pages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_shop(request, shop_id):
    try:
        if request.method == 'GET':
            shop = Shop.objects.get(id=shop_id)
            serializer = ShopSerializer(shop)
            return Response(serializer.data, status=status.HTTP_200_OK)

    except Shop.DoesNotExist:
        return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.exception("Error retrieving shop: %s", e)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PUT'])
def update_shop(request, shop_id):
    try:
        if request.method == 'PUT':
            shop = Shop.objects.get(id=shop_id)
            name = request.data.get('name', shop.name)
            template_id = request.data.get('template')
            modified_pages_data = request.data.get('modified_pages', {})

            print(f"Received request: shop_id={shop_id}, name={name}, template_id={template_id}, modified_pages={modified_pages_data}")

            if template_id:
                try:
                    template = Template.objects.get(id=template_id)
                    customized_template = CustomizedTemplate.objects.create(original_template=template, name=name)
                    shop.customized_template = customized_template
                except Template.DoesNotExist:
                    return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)

            shop.name = name
            shop.save()

            # Process modified pages
            for page_name, page_data in modified_pages_data.items():
                html = page_data.get('html')
                css = page_data.get('css')
                js = page_data.get('js', '') # Assuming JS is optional

                if html and css:
                    # Update or create a new customized page instance
                    customized_page, created = CustomizedPage.objects.update_or_create(
                        customized_template=shop.customized_template,
                        name=page_name,
                        defaults={'html': html, 'css': css, 'js': js}
                    )

            serializer = ShopSerializer(shop)
            return Response(serializer.data, status=status.HTTP_200_OK)

    except Shop.DoesNotExist:
        return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.exception("Error updating shop: %s", e)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def all_shops(request):
    shops = Shop.objects.all()
    serializer = ShopSerializer(shops, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_shop(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
    except Shop.DoesNotExist:
        return Response({"error": "Shop not found"}, status=404)

    serializer = ShopSerializer(shop)
    return Response(serializer.data)