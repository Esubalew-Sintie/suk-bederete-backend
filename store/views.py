from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from.models import Product
from merchant.models import Merchant
from category.models import ProductCategory
from.serializers import ProductSerializer
from rest_framework.parsers import  MultiPartParser

from rest_framework.pagination import PageNumberPagination
import random
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

class ProductManagementView(APIView):
   parser_classes = [MultiPartParser]  # Use MultiPartParser for file uploads

   def post(self, request, *args, **kwargs):
    try:
        products_data = request.data.get('products', [])
        merchantId = request.data.get('merchantId')
        try:
            merchant = Merchant.objects.get(unique_id=merchantId)
        except Merchant.DoesNotExist:
            return Response({"error": "Merchant not found"}, status=status.HTTP_404_NOT_FOUND)

        if not products_data:
            return Response({"error": "No products data provided"}, status=status.HTTP_400_BAD_REQUEST)

        validated_products = []

        for product_data in products_data:
            category_name = product_data.get('category')
            image = None
            if 'image' in request.FILES:
                image = request.FILES['image']
                product_data['image'] = image

            if not category_name or not merchant:
                logger.warning(f"Missing required data for product: {category_name} && {merchantId}")
                continue

            # Attempt to get the category based on slug and description
            category, created = ProductCategory.objects.get_or_create(catagory_name=category_name)
            if not category:
                logger.warning(f"Failed to find or create category for product: {category_name}")
            product_data['category'] = category.id
            product_data['productHolder'] = merchantId
            product_data['slug'] = category_name
                        # Adjusting the serializer initialization to pass the category object directly
            product_serializer = ProductSerializer(data=product_data)
            if product_serializer.is_valid():
                product = product_serializer.save()
                validated_products.append(product)
            else:
                logger.error(f"Validation error for product: {category.id}  {merchantId} && {product_serializer.errors}")

        return Response({
            "message": f"{len(validated_products)} products created successfully",
            "products": ProductSerializer(validated_products, many=True).data,
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.exception("An error occurred while processing the request.")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   
    # creating patch view for updating products coming as a list
   def patch(self, request, *args, **kwargs):
        try:
            products_data = request.data.get('products', [])
            merchantId = request.data.get('merchantId')
            try:
                merchant = Merchant.objects.get(unique_id=merchantId)
            except Merchant.DoesNotExist:
                return Response({"error": "Merchant not found"}, status=status.HTTP_404_NOT_FOUND)

            if not products_data:
                return Response({"error": "No products data provided"}, status=status.HTTP_400_BAD_REQUEST)

            updated_products = []

            for product_data in products_data:
                product_id = product_data.get('id')
                if not product_id:
                    logger.warning(f"Missing required data for product: {product_id}")
                    continue

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    logger.warning(f"Product not found with ID: {product_id}")
                    continue

                # Adjusting the serializer initialization to pass the category object directly
                product_serializer = ProductSerializer(product, data=product_data, partial=True)
                if product_serializer.is_valid():
                    product = product_serializer.save()
                    updated_products.append(product)
                else:
                    logger.error(f"Validation error for product: {product_id} && {product_serializer.errors}")

            return Response({
                "message": f"{len(updated_products)} products updated successfully",
                "products": ProductSerializer(updated_products, many=True).data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("An error occurred while processing the request.")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetProducts(APIView):
    def get(self, request, merchant_id, *args, **kwargs):
        category_slug = request.query_params.get('category', None)
        
        # Initialize the response data
        response_data = {}
        
        # Get random 4 products for 'featured' category added by the merchant
        all_products = list(Product.objects.filter(productHolder=merchant_id))  # Corrected here
        featured_products = random.sample(all_products, min(4, len(all_products)))
        
        # Get latest 8 products for 'new_arrival' category added by the merchant
        new_arrival_products = Product.objects.filter(productHolder=merchant_id).order_by('-created_at')[:8]  # And here
        
        # Get all products with pagination for 'all_products' category added by the merchant
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(Product.objects.filter(productHolder=merchant_id), request)  # And here
        all_products_paginated = ProductSerializer(result_page, many=True).data
        
        # Add serialized products to the response data
        response_data['featured'] = ProductSerializer(featured_products, many=True).data
        response_data['new_arrival'] = ProductSerializer(new_arrival_products, many=True).data
        response_data['all_products'] = all_products_paginated
        
        # Handle category filtering if provided
        if category_slug:
            filtered_products = Product.objects.filter(category__slug=category_slug, productHolder=merchant_id)  # And here
            response_data['filtered'] = ProductSerializer(filtered_products, many=True).data
        
        return Response(response_data, status=status.HTTP_200_OK)