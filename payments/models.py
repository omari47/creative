from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Payment(models.Model):
    """Payment records for movie purchases/rentals"""
    PAYMENT_METHODS = (
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
        ('direct', 'Direct'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # For M-Pesa
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)  # For M-Pesa
    paypal_payment_id = models.CharField(max_length=100, blank=True, null=True)  # For PayPal
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.amount}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']


class NewsletterSubscription(models.Model):
    """Newsletter subscription records"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'