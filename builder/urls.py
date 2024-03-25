from django.urls import path
from . import views

urlpatterns = [
    path('getTemplate/', views.getTemplate, name="gettemplate")
]