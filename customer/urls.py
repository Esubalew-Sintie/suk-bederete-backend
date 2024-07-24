from django.urls import path
from.views import CustomerList, CustomerDetail, CustomerUpdate, CustomerDelete, CustomerCreate,register,login,CustomerListView,get_customer,CustomerUpdateView

urlpatterns = [
    path('customer/register/', register, name='customer-register'),
    path('customer/login/', login, name='customer-login'),
    path('customers/', CustomerList.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
    path('customers/update/<int:pk>/', CustomerUpdate.as_view(), name='customer-update'),
    path('customers/delete/<int:pk>/', CustomerDelete.as_view(), name='customer-delete'),
    path('customers/create/', CustomerCreate.as_view(), name='customer-crMerchantListVieweate'),
    path('customers/', CustomerListView.as_view(), name='update_customer'),
    path('customer/<uuid:unique_id>/', get_customer, name='get_merchant'),
    path('customer/update/<uuid:unique_id>/', CustomerUpdateView.as_view(), name='update_customer'),

]
