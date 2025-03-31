import logging
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    import paypalrestsdk
    from paypalrestsdk import Payment

    # Configure PayPal SDK
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,  # "sandbox" or "live"
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET
    })
except ImportError:
    logger.warning("PayPalRESTSDK not installed. PayPal functionality will be limited.")


def create_payment(movie_title, price, return_url, cancel_url):
    """
    Create a PayPal payment
    """
    try:
        if 'paypalrestsdk' not in globals():
            raise ImportError("PayPalRESTSDK not installed")

        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": movie_title,
                        "sku": "movie",
                        "price": str(price),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(price),
                    "currency": "USD"
                },
                "description": f"Purchase of {movie_title}"
            }]
        })

        if payment.create():
            return payment
        else:
            logger.error(f"Failed to create PayPal payment: {payment.error}")
            return None
    except Exception as e:
        logger.error(f"Error creating PayPal payment: {str(e)}")
        raise


def execute_payment(payment_id, payer_id):
    """
    Execute a PayPal payment after user approval
    """
    try:
        if 'paypalrestsdk' not in globals():
            raise ImportError("PayPalRESTSDK not installed")

        payment = Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            return True
        else:
            logger.error(f"Failed to execute PayPal payment: {payment.error}")
            return False
    except Exception as e:
        logger.error(f"Error executing PayPal payment: {str(e)}")
        raise