from django.urls import path
from.views import CustomerList, CustomerDetail, CustomerUpdate, CustomerDelete, CustomerCreate,register,login

urlpatterns = [
    path('customers/register/', register, name='customer-register'),
    path('customers/login/', login, name='customer-login'),
    path('customers/', CustomerList.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
    path('customers/update/<int:pk>/', CustomerUpdate.as_view(), name='customer-update'),
    path('customers/delete/<int:pk>/', CustomerDelete.as_view(), name='customer-delete'),
    path('customers/create/', CustomerCreate.as_view(), name='customer-create'),
]
