import json
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.http import StreamingHttpResponse
from django.views import View
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from.models import Order  
from.serializers import OrderSerializer

class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
# Make sure to import your Order model

def event_stream():
    initial_data = ""
    while True:
        data = json.dumps(list(Order.objects.order_by("-id").values("product", "amount", "status","paymentStatus","payment","shippingMethod","amount","date","placedBy")), cls=DjangoJSONEncoder)
        if not initial_data == data:
            yield "\ndata: {}\n\n".format(data)
            initial_data = data
        time.sleep(1)


class OrderStreamView(View):
    def get(self, request):
        response = StreamingHttpResponse(event_stream())
        response['Content-Type'] = 'text/event-stream'
        return response


# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.contrib.auth.mixins import LoginRequiredMixin
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes
# from.models import Order
# from.serializers import OrderSerializer
# from django.core.serializers.json import DjangoJSONEncoder
# import json
# import time

# @method_decorator(login_required, name='dispatch')
# class OrderStreamView(LoginRequiredMixin, View):
#     @api_view(['GET'])
#     @permission_classes([IsAuthenticated])
#     def get(self, request):
#         # Assuming the user's merchant ID is stored in a session variable or passed in some way
#         merchant_id = request.user.merchant_id  # This needs to be implemented based on your user model
#         response = StreamingHttpResponse(event_stream(merchant_id))
#         response['Content-Type'] = 'text/event-stream'
#         return response

# def event_stream(merchant_id):
#     initial_data = ""
#     while True:
#         # Filter orders based on the merchant_id
#         orders = Order.objects.filter(merchant_id=merchant_id).order_by("-id")
#         data = json.dumps(list(orders.values("product", "amount", "status","paymentStatus","payment","shippingMethod","amount","date","placedBy")), cls=DjangoJSONEncoder)
#         if not initial_data == data:
#             yield "\ndata: {}\n\n".format(data)
#             initial_data = data
#         time.sleep(1)

# # Note: The above code assumes that you have a way to associate a merchant ID with each user.
# # You might need to adjust the logic based on how your application handles user authentication and merchant IDs.
