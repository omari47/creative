from django.contrib import admin
from .models import Workshop
@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    # Adjust fields based on your actual model
    list_display = ('title', 'date', 'price', 'location')
    list_filter = ('date',)  # Keep only fields that exist
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'  # Keep if 'date' exists