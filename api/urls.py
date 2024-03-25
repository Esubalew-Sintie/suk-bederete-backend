from django.urls import path
from . import views
urlpatterns = [
    path('getroute/', views.getroutes, name="getroute" )
]