from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from django.http import JsonResponse
from .models import Product
from merchant.models import Merchant
from category.models import ProductCategory
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, JSONParser
import time
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
import json
import time
from django.http import StreamingHttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import random
import logging
from django.utils.text import slugify
from django.db.models import Sum  # Import Sum from django.db.models


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

class ProductManagementView(APIView):
    parser_classes = [MultiPartParser, JSONParser]  # Use MultiPartParser for file uploads and JSONParser for JSON data

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

                # Generate a unique slug
                base_slug = slugify(category_name)
                unique_slug = f"{base_slug}-{int(time.time())}"
                product_data['slug'] = unique_slug

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
        
        response_data = {}
        
        merchant = get_object_or_404(Merchant, unique_id=merchant_id)
        
        all_products = list(Product.objects.filter(productHolder=merchant).order_by('id'))
        
        try:
            featured_products = random.sample(all_products, min(4, len(all_products)))
        except ValueError:
            featured_products = all_products
        
        new_arrival_products = Product.objects.filter(productHolder=merchant).order_by('-created_at')[:8]
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(Product.objects.filter(productHolder=merchant).order_by('id'), request)
        all_products_paginated = ProductSerializer(result_page, many=True).data
        
        response_data['featured'] = ProductSerializer(featured_products, many=True).data
        response_data['new_arrival'] = ProductSerializer(new_arrival_products, many=True).data
        response_data['all_products'] = all_products_paginated
        
        if category_slug:
            filtered_products = Product.objects.filter(category__slug=category_slug, productHolder=merchant).order_by('id')
            response_data['filtered'] = ProductSerializer(filtered_products, many=True).data
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    
    
def check_stock_levels(request, merchant_id):
    products = Product.objects.filter(productHolder=merchant_id)
    out_of_stock_products = [product for product in products if product.stock == 0]
    response_data = {
        'out_of_stock_products': [
            {'id': product.id, 'name': product.name, 'stock': product.stock}
            for product in out_of_stock_products
        ]
    }
    return JsonResponse(response_data)

def event_stream(merchant_id):
    initial_data = list(Product.objects.filter(productHolder=merchant_id, stock=0))

    while True:
        current_data = list(Product.objects.filter(productHolder=merchant_id, stock=0))
        new_out_of_stock = [product for product in current_data if product not in initial_data]

        if new_out_of_stock:
            data = json.dumps([{
                'id': product.id,
                'name': product.name,
                'stock': product.stock,
                'message': f"{product.name} is out of stock."
            } for product in new_out_of_stock], cls=DjangoJSONEncoder)
            yield f"data: {data}\n\n"

        initial_data = current_data
        time.sleep(5)

class ProductStockStreamView(View):
    def get(self, request, merchant_id):
        merchant = get_object_or_404(Merchant, unique_id=merchant_id)
        response = StreamingHttpResponse(event_stream(merchant.unique_id))
        response['Content-Type'] = 'text/event-stream'
        return response
    
    
    
    
# View to check total stock levels
class TotalStockView(View):
    def get(self, request, merchant_id):
        merchant = get_object_or_404(Merchant, unique_id=merchant_id)
        total_stock = Product.objects.filter(productHolder=merchant).aggregate(total_stock=Sum('stock'))['total_stock']
        if total_stock is None:
            total_stock = 0  # In case there are no products or all have zero stock
        return JsonResponse({'total_stock': total_stock})

# View to get total categories
class TotalCategoriesView(View):
    def get(self, request, merchant_id):
        merchant = get_object_or_404(Merchant, unique_id=merchant_id)
        total_categories = Product.objects.filter(productHolder=merchant).values('category').distinct().count()
        return JsonResponse({'total_categories': total_categories})
    