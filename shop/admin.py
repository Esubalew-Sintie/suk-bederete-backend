from django.contrib import admin
from .models import Shop, CustomizedTemplate, CustomizedPage
# Register your models here.
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date')


admin.site.register(Shop, ShopAdmin)
admin.site.register(CustomizedTemplate)
admin.site.register(CustomizedPage)