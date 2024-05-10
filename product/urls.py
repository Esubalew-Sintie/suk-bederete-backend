from django.urls import path
from.views import ProductListCreateView, ProductRetrieveUpdateDestroyView,ProductStreamView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
    path('stream/', ProductStreamView.as_view(), name='sse_stream'),

]
