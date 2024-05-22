from django.urls import path
from . import views


urlpatterns = [
    path('upload/', views.PictureUploadView.as_view(), name='upload-screenshot'),
    path('customized_template/', views.save_customized_pages, name='customized_shop'),
    path('getcustomized_template/<uuid:merchant_id>/', views.get_customizedTemplate, name='get_customized_shop'),
    path('getcustomised_pages/<uuid:merchant_id>/', views.get_customizedPages, name='get_customized_pages'),
    path('getcustomised_page/<int:template_id>/<str:page_name>/', views.get_customizedPage, name='get_customized_page'),
    path('updatecustomised_pages/<int:template_id>/', views.update_customized_pages, name='update_customized_pages'),
    path('getshop/<uuid:shop_id>/', views.get_shop, name='get_shop'),
    path('getshops/', views.get_shops, name='get_shops'),
    path('publishshop/', views.create_shop, name='publish_shop'),
    

    # path('create_shop/', views.create_shop, name='create_shop'),
    # path('getshop/<int:shop_id>/', views.get_shop, name='get_shop'),
    # path('updateshop/<int:shop_id>/', views.update_shop, name='update_shop'),
    # path('shops/', views.all_shops, name='all_shops'),
    # path('shops/<int:shop_id>/', views.get_shop, name='get_shop'),
    # path('shops/<int:shop_id>/update/', views.update_shop, name='update_shop'),
]