from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('merchant/update/<uuid:unique_id>/', views.MerchantUpdateView.as_view(), name='update_merchant'),
    

]