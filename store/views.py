from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from.models import Product
from merchant.models import Merchant
from category.models import ProductCategory
from.serializers import ProductSerializer
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

class ProductManagementView(APIView):
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
            # image = None
            # if 'image' in request.FILES:
            #     image = request.FILES['image']

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

   def get(self, request, *args, **kwargs):
        # Retrieve products
        category_slug = request.query_params.get('category', None)

        if category_slug:
            # Filter products by category slug
            products = Product.objects.filter(category__slug=category_slug)
        else:
            # Return all products if no category filter is applied
            products = Product.objects.all()

        # Serialize the queryset
        product_serializer = ProductSerializer(products, many=True)

        return Response(product_serializer.data,status=status.HTTP_200_OK)
