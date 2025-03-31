from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
import uuid
import json

from .models import Payment
from movies.models import Movie
from .services.mpesa import MpesaClient
from .services.paypal import create_payment as create_paypal_payment, execute_payment as execute_paypal_payment


@login_required
def payment_view(request, movie_id):
    """Display payment form for a movie"""
    movie = get_object_or_404(Movie, id=movie_id)

    # Check if user already paid
    user_payments = Payment.objects.filter(
        user=request.user,
        movie=movie,
        status='completed'
    )

    if user_payments.exists():
        # User already paid for this movie
        return redirect('movies:watch', movie_id=movie_id)

    context = {
        'movie': movie,
    }
    return render(request, 'payments/payment.html', context)


@login_required
def process_payment(request, movie_id):
    """Process the payment based on selected method"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    movie = get_object_or_404(Movie, id=movie_id)
    payment_method = request.POST.get('payment_method')

    # Generate a unique transaction ID
    transaction_id = f"TX-{uuid.uuid4().hex[:8].upper()}"

    # Create a pending payment record
    payment = Payment.objects.create(
        user=request.user,
        movie=movie,
        amount=movie.price,
        method=payment_method,
        transaction_id=transaction_id,
        status='pending'
    )

    if payment_method == 'mpesa':
        # Process M-Pesa payment
        phone_number = request.POST.get('phone_number')

        if not phone_number:
            return JsonResponse({'error': 'Phone number is required for M-Pesa payments'}, status=400)

        payment.phone_number = phone_number
        payment.save()

        try:
            mpesa_client = MpesaClient()
            callback_url = request.build_absolute_uri(reverse('payments:mpesa_callback'))

            response = mpesa_client.stk_push(
                phone_number=phone_number,
                amount=float(movie.price),
                callback_url=callback_url,
                account_reference=f"Sanaa Mtaani - {movie.title}",
                transaction_desc=f"Payment for {movie.title}"
            )

            if 'CheckoutRequestID' in response:
                # Store the checkout request ID for callback verification
                payment.checkout_request_id = response['CheckoutRequestID']
                payment.save()

                return JsonResponse({
                    'success': True,
                    'message': 'M-Pesa payment initiated. Please check your phone to complete payment.'
                })
            else:
                payment.status = 'failed'
                payment.save()
                return JsonResponse({'error': 'Failed to initiate M-Pesa payment'}, status=400)

        except Exception as e:
            payment.status = 'failed'
            payment.save()
            return JsonResponse({'error': str(e)}, status=400)

    elif payment_method == 'paypal':
        # Process PayPal payment
        return_url = request.build_absolute_uri(
            reverse('payments:paypal_success') + f'?payment_id={payment.id}'
        )
        cancel_url = request.build_absolute_uri(reverse('payments:paypal_cancel'))

        try:
            paypal_payment = create_paypal_payment(
                movie_title=movie.title,
                price=float(movie.price),
                return_url=return_url,
                cancel_url=cancel_url
            )

            if paypal_payment:
                # Store PayPal payment ID
                payment.paypal_payment_id = paypal_payment.id
                payment.save()

                # Redirect to PayPal
                for link in paypal_payment.links:
                    if link.rel == 'approval_url':
                        return JsonResponse({
                            'success': True,
                            'redirect_url': link.href
                        })

            payment.status = 'failed'
            payment.save()
            return JsonResponse({'error': 'Failed to create PayPal payment'}, status=400)

        except Exception as e:
            payment.status = 'failed'
            payment.save()
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Invalid payment method'}, status=400)


@csrf_exempt
def mpesa_callback(request):
    """Callback for M-Pesa payments"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result_code = data['Body']['stkCallback']['ResultCode']
            checkout_request_id = data['Body']['stkCallback']['CheckoutRequestID']

            # Find the payment by checkout_request_id
            payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()

            if payment:
                if result_code == 0:
                    # Payment successful
                    payment.status = 'completed'
                    payment.save()
                else:
                    # Payment failed
                    payment.status = 'failed'
                    payment.save()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def paypal_success(request):
    """Handle PayPal payment success"""
    payment_id = request.GET.get('payment_id')
    paypal_payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not paypal_payment_id or not payer_id:
        messages.error(request, 'Invalid payment information')
        return redirect('core:home')

    payment = get_object_or_404(Payment, id=payment_id, paypal_payment_id=paypal_payment_id)

    try:
        # Execute PayPal payment
        if execute_paypal_payment(paypal_payment_id, payer_id):
            payment.status = 'completed'
            payment.save()
            messages.success(request, 'Payment completed successfully')
            return redirect('movies:watch', movie_id=payment.movie.id)
        else:
            payment.status = 'failed'
            payment.save()
            messages.error(request, 'Payment execution failed')
            return redirect('movies:detail', movie_id=payment.movie.id)

    except Exception as e:
        payment.status = 'failed'
        payment.save()
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('movies:detail', movie_id=payment.movie.id)


def paypal_cancel(request):
    """Handle PayPal payment cancellation"""
    messages.info(request, 'Payment was cancelled')
    return redirect('core:home')


@login_required
def payment_history(request):
    """View payment history for the user"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    context = {'payments': payments}
    return render(request, 'payments/history.html', context)


@login_required
def check_payment(request, payment_id):
    """Check the status of a payment"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    if payment.status != 'pending':
        return redirect('payments:history')

    if payment.method == 'mpesa' and payment.checkout_request_id:
        try:
            mpesa_client = MpesaClient()
            response = mpesa_client.check_payment_status(payment.checkout_request_id)

            result_code = response.get('ResultCode')
            if result_code == 0:
                payment.status = 'completed'
                payment.save()
                messages.success(request, 'Payment completed successfully.')
                return redirect('movies:watch', movie_id=payment.movie.id)
            elif result_code == 1032:  # Transaction canceled
                payment.status = 'failed'
                payment.save()
                messages.error(request, 'M-Pesa transaction was canceled.')
            else:
                messages.info(request, 'Payment is still being processed. Please check again later.')
        except Exception as e:
            messages.error(request, f'Error checking payment status: {str(e)}')

    return redirect('payments:history')


@login_required
def retry_payment(request, movie_id):
    """Retry a failed payment"""
    # Find and cancel any pending payments for this movie
    pending_payments = Payment.objects.filter(
        user=request.user,
        movie_id=movie_id,
        status='pending'
    )

    for payment in pending_payments:
        payment.status = 'failed'
        payment.save()

    return redirect('payments:process', movie_id=movie_id)