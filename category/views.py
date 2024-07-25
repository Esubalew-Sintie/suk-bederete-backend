from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ShopCategory
from .serializer import ShopCategorySerializer
# Create your views here.
#write me view to send all the shop categories to the frontend


@api_view(['GET'])
def get_shop_category(request):
    shop_categories = ShopCategory.objects.all()
    serializer = ShopCategorySerializer(shop_categories, many=True)
    return Response(serializer.data)