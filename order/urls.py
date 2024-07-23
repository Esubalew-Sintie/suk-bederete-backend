from . import views
from django.urls import path
from.views import OrderStreamView ,OrderCreateView, MerchantOrdersView,OrderListView

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<uuid:merchant_id>/', MerchantOrdersView.as_view(), name='order-list'),
    # path('orders/<int:pk>/', OrderUpdateDestroyView.as_view(), name='order-detail'),
    path('stream/<uuid:merchant_id>/', OrderStreamView.as_view(), name='sse_stream'),
     path('all-orders/', OrderListView.as_view(), name='order-list'),

]
