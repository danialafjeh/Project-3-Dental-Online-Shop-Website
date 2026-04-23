from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from . import models

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Brand)
admin.site.register(models.UserDeliveryInfo)
admin.site.register(models.ShopInfo)

class ProfileInLine(admin.StackedInline):
    model = models.UserDeliveryInfo

class UserAdmin(DefaultUserAdmin):
    model = User
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'password'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    inlines = [ProfileInLine]
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
