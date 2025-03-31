from django.contrib import admin
from .models import Payment, NewsletterSubscription

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Adjust based on your actual fields
    list_display = ('user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')  # Remove payment_type
    search_fields = ('user__username', 'transaction_id')
    date_hierarchy = 'created_at'

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    # Adjust based on your actual fields
    list_display = ('email', 'created_at')  # Changed subscribed_at to created_at
    search_fields = ('email',)
    date_hierarchy = 'created_at'  # Changed subscribed_at to created_at