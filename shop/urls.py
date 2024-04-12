from django.urls import path
from . import views
urlpatterns = [
    path('customized_template/', views.save_customized_pages, name='customized_shop'),
    path('getcustomized_template/<int:customised_TemplateId>/', views.get_customizedTemplate, name='get_customized_shop'),
    # path('create_shop/', views.create_shop, name='create_shop'),
    path('getshop/<int:shop_id>/', views.get_shop, name='get_shop'),
    path('updateshop/<int:shop_id>/', views.update_shop, name='update_shop'),
    path('shops/', views.all_shops, name='all_shops'),
    path('shops/<int:shop_id>/', views.get_shop, name='get_shop'),
]