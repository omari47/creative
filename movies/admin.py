from django.contrib import admin
from .models import Movie, Trailer

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # Adjust these fields based on what actually exists in your Movie model
    list_display = ('title', 'created_at', 'price', 'is_featured')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'  # Use created_at instead of release_date

@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'