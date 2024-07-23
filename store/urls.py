from . import views
from django.urls import path
from.views import ProductManagementView,GetProducts,check_stock_levels,ProductStockStreamView,TotalStockView,TotalCategoriesView

urlpatterns = [
    path('product/', ProductManagementView.as_view(), name='product-create'),
    path('product/<uuid:merchant_id>/', GetProducts.as_view(), name='get products'),
    path('product/stock/<uuid:merchant_id>/', check_stock_levels, name='get products_stcoks'),
    path('product/stock/stream/<uuid:merchant_id>/', ProductStockStreamView.as_view(), name='get product_stocks_stream'),
    path('product/<uuid:merchant_id>/total-stock/', TotalStockView.as_view(), name='total-stock'),
    path('product/<uuid:merchant_id>/total-categories/', TotalCategoriesView.as_view(), name='total-categories'),

    # path('orders/<str:merchant_id>/', MerchantOrdersView.as_view(), name='order-list'),
    # path('orders/<int:pk>/', OrderUpdateDestroyView.as_view(), name='order-detail'),
    # path('stream/<str:merchant_id>/', OrderStreamView.as_view(), name='sse_stream'),
]
