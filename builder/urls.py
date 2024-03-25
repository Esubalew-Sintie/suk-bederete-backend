from django.urls import path
from . import views

urlpatterns = [
    path('getTemplate/', views.getTemplates, name="gettemplates"),
    path('getTemplate/<int:pk>/', views.getTemplate, name="gettemplate")
]