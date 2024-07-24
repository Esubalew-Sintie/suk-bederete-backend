from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('merchant/update/<uuid:unique_id>/', views.MerchantUpdateView.as_view(), name='update_merchant'),
    path('merchants/', views.MerchantListView.as_view(), name='update_merchant'),
    path('merchant/<uuid:unique_id>/', views.get_merchant, name='get_merchant'),
]