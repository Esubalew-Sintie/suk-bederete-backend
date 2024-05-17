from django.urls import path
from . import views

urlpatterns = [
    path('getTemplate/', views.getTemplates, name="gettemplates"),
    path('getTemplate/<int:pk>/', views.getTemplate, name="gettemplate"),
    path('getTemplatePage/<int:pk>/', views.getTemplatePages, name="gettemplatepage"),
    path('getTemplatePages/<int:template_id>/', views.getTemplatePage, name="gettemplatepages"),
    path('getPage/<int:template_id>/<int:page_id>/', views.getePage, name="getepage"),
    path('updatePageContent/<int:template_id>/<int:page_id>/', views.updatePageContent, name="updatePageContent")
]