from . import views
from django.urls import path
from.views import ProductManagementView

urlpatterns = [
    path('product/', ProductManagementView.as_view(), name='product-create'),
    # path('orders/<str:merchant_id>/', MerchantOrdersView.as_view(), name='order-list'),
    # path('orders/<int:pk>/', OrderUpdateDestroyView.as_view(), name='order-detail'),
    # path('stream/<str:merchant_id>/', OrderStreamView.as_view(), name='sse_stream'),
]
