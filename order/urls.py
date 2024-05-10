from django.urls import path
from . import views
from django.urls import path
from.views import OrderStreamView , OrderListCreateView, OrderRetrieveUpdateDestroyView

urlpatterns = [
     path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('stream/', OrderStreamView.as_view(), name='sse_stream'),
]
