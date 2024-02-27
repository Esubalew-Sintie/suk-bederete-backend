from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.

class Accountadmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'is_active', 'date_joined')
    list_display_links = ('email', 'first_name')
    readonly_fields = ('password', 'last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, Accountadmin)