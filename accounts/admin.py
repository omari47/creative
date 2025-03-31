from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from pip._vendor.packaging.utils import _

from .models import User

class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Info'), {'fields': ('phone_number', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {'fields': ('phone_number', 'profile_image')}),
    )

admin.site.register(User, CustomUserAdmin)