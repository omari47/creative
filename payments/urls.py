from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('<int:movie_id>/', views.payment_view, name='process'),
    path('<int:movie_id>/process/', views.process_payment, name='process_payment'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('paypal/success/', views.paypal_success, name='paypal_success'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
    path('history/', views.payment_history, name='history'),
    path('check/<int:payment_id>/', views.check_payment, name='check'),
    path('retry/<int:movie_id>/', views.retry_payment, name='retry'),
]