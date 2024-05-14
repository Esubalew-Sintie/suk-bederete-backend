import json
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.http import StreamingHttpResponse
from django.views import View
from rest_framework import generics
from.models import Product
from.serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]  # Removed

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]  # Removed

def event_stream():
    initial_data = ""
    while True:
        # Query products with quantity zero
        products = Product.objects.filter(quantity=0).order_by("-id")
        data = json.dumps(list(products.values("name", "quantity", "category")), cls=DjangoJSONEncoder)
        if not initial_data == data:
            yield "\ndata: {}\n\n".format(data)
            initial_data = data
        time.sleep(1)
        
class ProductStreamView(View):
    def get(self, request):
        response = StreamingHttpResponse(event_stream())
        response['Content-Type'] = 'text/event-stream'
        return response
