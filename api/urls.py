from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('getroute/', views.getroutes, name="getroute" ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', views.VerifyTokenView.as_view(), name='token_verify'),
    path('update-metadata/<str:user_id>/<str:role>/', views.update_clerk_user_metadata, name='update_metadata'),


]