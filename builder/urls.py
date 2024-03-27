from django.urls import path
from .views import TemplateUpdateAPIView ,getTemplate,getTemplates

urlpatterns = [
    path('getTemplate/',getTemplates, name="gettemplates"),
    path('getTemplate/<int:pk>/', getTemplate, name="gettemplate"),
    path('<int:pk>/',TemplateUpdateAPIView.as_view(), name="update-template")
]