from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Shop, CustomizedTemplate, CustomizedPage
from .serializer import ShopSerializer,ScreenshotCreateSerializer, CustomizedPageSerializer, CustomizedTemplateSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from builder.models import Template
from django.shortcuts import get_object_or_404
from merchant.models import Merchant
import logging
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from.models import Screenshot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import os
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from.serializer import PictureUploadSerializer
from django.conf import settings
from django.core.files.storage import default_storage
from.models import Picture
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

DEFAULT_IMAGE_URL = 'media/shop/shop_preview_default.jpg'

def generate_picture_urls(pictures):
    urls = []
    # print(pictures)
    for picture in pictures:
        # Get the original filename
        original_filename = picture.image.name
        
        # Generate the URL for the image
        url = f"http://localhost:8000//{settings.MEDIA_URL}{original_filename}"
        
        # Append the URL to the list
        urls.append(url)
    
    return urls


class PictureUploadView(APIView):
    parser_classes = [MultiPartParser]  # Use MultiPartParser for file uploads

    def post(self, request, *args, **kwargs):
        serializer = PictureUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Instead of calling serializer.save() directly, you need to handle the files manually
            files = request.FILES.getlist('files')
            pictures = []
            for file in files:
                picture = Picture(image=file)  # Create a new Picture instance for each file
                picture.save()  # Save the instance to the database
                pictures.append(picture)  # Add the instance to the list
            
            # Now, pictures is a list of Picture instances, so we can pass it to generate_picture_urls
            picture_urls = generate_picture_urls(pictures)
            return Response(picture_urls, status=200)
        else:
            # Return a response indicating validation failed
            return Response(serializer.errors, status=400)
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        responses = []  
        print(files)
        # List to collect all responses
        for file in files:
            print(file.name)
            # Save the file to a temporary location
            temp_path = default_storage.save(file.name, file)
            
            # Optionally, move the file to a more permanent location
            # For simplicity, we'll just keep it in the temporary folder
            final_path = temp_path
            
            # Collect the response for each file
            responses.append({'urls': f'{settings.MEDIA_URL}{final_path}'})
        
        # Return a single JSON response containing all file URLs
        return JsonResponse(responses, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


class SaveScreenshot(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ScreenshotCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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

            print(f"Received request: template={template}")
            print(f'recevied modifiedpages :{modified_pages_data}')

            if not template or not modifier:
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    # Create a new customized template for each modifier and template pair
                    customized_template = CustomizedTemplate.objects.create(
                        original_template=template,
                        modifiedby=modifier
                    )

                    # Process modified pages
                    for page_name, page_data in modified_pages_data.items():
                        html = page_data.get('html')
                        css = page_data.get('css')
                        js = page_data.get('js', '')  # Assuming JS is optional

                        if html and css:
                            # Create a new customized page instance
                            CustomizedPage.objects.create(
                                customized_template=customized_template,
                                name=page_name,
                                html=html,
                                css=css,
                                js=js
                            )
            except ObjectDoesNotExist:
                return Response({"error": "Template or Customized template not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Customized pages saved successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception("Error saving customized pages: %s", e)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#create view to update customised pages with the given customised templateId

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_customized_pages(request, template_id):
    try:
        # Get the customized template
        customized_template = get_object_or_404(CustomizedTemplate, pk=template_id)
        if request.method == 'POST':

            modified_pages_wrapper = request.data.get('modified_pages')
            modified_pages_data = modified_pages_wrapper.get('modifiedPages')
            

        if not modified_pages_data:
            return Response({"error": "No modified pages data provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        

        with transaction.atomic():
            # Process modified pages
            for page_name, page_data in modified_pages_data.items():
                htmlcontent = page_data.get('html')
                csscontent = page_data.get('css')
                jscontent = page_data.get('js')
                
                if htmlcontent and csscontent:
                    # Update or create the customized page instance
                    # CustomizedPage.objects.update_or_create(
                    #     customized_template=customized_template,
                    #     name=page_name,
                    #     defaults={
                    #         'html': htmlcontent,
                    #         'css': csscontent,
                    #         'js': jscontent
                    #     }
                    # )
                    try:
                        page = CustomizedPage.objects.get(customized_template=customized_template, name=page_name)
                        page.html = htmlcontent
                        page.css = csscontent
                        page.js = jscontent
                        page.save()
                    except CustomizedPage.DoesNotExist:
                        return Response({"error": "Customized Page not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Customized pages updated successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception("Error updating customized pages: %s", e)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_customizedTemplate(request, merchant_id):
    logger.info(f"Received request for CustomizedTemplate modified by Merchant with ID: {merchant_id}")
    try:
        customised_Template = CustomizedTemplate.objects.get(modifiedby__unique_id=merchant_id)
    except CustomizedTemplate.DoesNotExist:
        logger.error(f"No CustomizedTemplate found modified by Merchant with ID: {merchant_id}")
        return Response({"error": "No CustomizedTemplate found modified by the given Merchant ID"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomizedTemplateSerializer(customised_Template, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_shop(request):
    try:
        # Get data from the request
        name = request.data.get('name')
        customized_template_id = request.data.get('customised_template')
        preview_image = request.data.get('preview_image', None)

        print(f"Received request: name={name}, customized_template_id={customized_template_id}, preview_image={preview_image}")
        
        # Validate if name is provided
        if not name:
            return Response({"error": "Name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the authenticated user (merchant)
        owner = request.user
        
        # Check if the user is a merchant
        if not hasattr(owner, 'merchant'):
            return Response({"error": "Authenticated user is not a merchant."}, status=status.HTTP_403_FORBIDDEN)
        
        # Get the customized template
        customized_template = get_object_or_404(CustomizedTemplate, pk=customized_template_id)

        if preview_image is None:
            preview_image = DEFAULT_IMAGE_URL
        
        # Create the shop with only the name
        shop, created = Shop.objects.update_or_create(
            name=name, 
            owner=owner.merchant,  # Assuming owner is related to merchant
            preview_image=preview_image, 
            customized_template=customized_template
        )
        
        # Serialize the created shop
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.exception("Error creating shop: %s", e)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

#create a view to get a single page with the given template_id and page_id
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_customizedPage(request, template_id, page_name):
    try:
        customized_page = CustomizedPage.objects.get(customized_template=template_id, name=page_name)
    except CustomizedPage.DoesNotExist:
        return Response({"error": "Customized Page not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CustomizedPageSerializer(customized_page, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_customizedPages(request, merchant_id):
    try:
        print(merchant_id)
        customized_template = CustomizedTemplate.objects.get(modifiedby__unique_id=merchant_id)
    except CustomizedTemplate.DoesNotExist:
        return Response({"error": "Customized Template not found"}, status=status.HTTP_404_NOT_FOUND)
    
    pages = CustomizedPage.objects.filter(customized_template=customized_template)
    serializer = CustomizedPageSerializer(pages, many=True)
    return Response(serializer.data)
   
# Helper function to update shop statuses
def update_shops_status(shops):
    for shop in shops:
        shop.check_payment_status()

# Get all shops
@api_view(['GET'])
@permission_classes([AllowAny])
def get_shops(request):
    shops = Shop.objects.all()
    update_shops_status(shops)  # Update status and suspense for all shops
    serializer = ShopSerializer(shops, many=True)
    return Response(serializer.data)

# Send customized pages of a customized template associated with the given shop_id
@api_view(['GET'])
@permission_classes([AllowAny])
def get_shop(request, shop_id):
    try:
        shop = Shop.objects.get(unique_id=shop_id)
    except Shop.DoesNotExist:
        return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)
    
    shop.check_payment_status()  # Update status and suspense for the specific shop
    
    customized_template = shop.customized_template
    if not customized_template:
        return Response({"error": "Customized Template not found"}, status=status.HTTP_404_NOT_FOUND)
    
    pages = CustomizedPage.objects.filter(customized_template=customized_template)
    serializer = CustomizedPageSerializer(pages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([AllowAny])
def get_shop_Id(request, shop_id):
    try:
        shop = Shop.objects.get(unique_id=shop_id)
    except Shop.DoesNotExist:
        return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

    shop.check_payment_status()  # Update status and suspense for the specific shop
    serializer = ShopSerializer(shop, many=False)
    print(serializer.data)
    return Response(serializer.data)

# Creating a view to verify if the given merchant_id is associated with a shop
@api_view(['GET'])
@permission_classes([AllowAny])
def get_shop_by_merchant(request, merchant_id):
    try:
        merchant = Merchant.objects.get(unique_id=merchant_id)
    except Merchant.DoesNotExist:
        return Response({"error": "Merchant not found"}, status=status.HTTP_404_NOT_FOUND)
    
    shops = Shop.objects.filter(owner=merchant)
    if not shops.exists():
        return Response({"error": "No shops found for this merchant"}, status=status.HTTP_404_NOT_FOUND)
    
    update_shops_status(shops)  # Update status and suspense for all shops belonging to the merchant
    serializer = ShopSerializer(shops, many=True)
    return Response(serializer.data)


class UpdateShopPreviewImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, merchant_id):
        try:
            merchant = Merchant.objects.get(unique_id=merchant_id)
            shop = Shop.objects.get(owner=merchant)
        except Merchant.DoesNotExist:
            return Response({'error': 'Merchant not found'}, status=status.HTTP_404_NOT_FOUND)
        except Shop.DoesNotExist:
            return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
        print(request.data,"image data")
        serializer = ShopSerializer(shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("preview image updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        print("preview image updated failed")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def suspend_shop(request, unique_id):
    try:
        shop = Shop.objects.get(unique_id=unique_id)
    except Shop.DoesNotExist:
        return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ShopSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['suspense']:
            shop.suspend()
        else:
            shop.unsuspend()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopListView(generics.ListAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        # Fetch all shops and prefetch related data
        shops = Shop.objects.all().prefetch_related('owner')
        for shop in shops:
            shop.check_payment_status()
            shop.save()  # Ensure the updated status is saved
        return shops

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
