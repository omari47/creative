import requests
import base64
import datetime
from django.conf import settings


class MpesaClient:
    """
    Class to handle M-Pesa API integrations
    """

    def __init__(self):
        self.business_shortcode = settings.MPESA_SHORTCODE
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.base_url = "https://sandbox.safaricom.co.ke" if settings.MPESA_ENVIRONMENT == "sandbox" else "https://api.safaricom.co.ke"
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """Get OAuth access token from Safaricom"""
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode("utf-8")
        headers = {
            "Authorization": f"Basic {auth}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
            return response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            # In production, you might want to log this error
            raise Exception(f"Failed to get M-Pesa access token: {str(e)}")

    def format_phone_number(self, phone_number):
        """
        Format the phone number to the required format (254XXXXXXXXX)
        """
        if phone_number.startswith("+"):
            phone_number = phone_number[1:]
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]
        if not phone_number.startswith("254"):
            phone_number = "254" + phone_number
        return phone_number

    def stk_push(self, phone_number, amount, callback_url, account_reference, transaction_desc):
        """
        Initiate STK Push transaction
        """
        if not self.access_token:
            raise Exception("Access token not available")

        phone_number = self.format_phone_number(phone_number)

        # Generate password
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = f"{self.business_shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode("utf-8")

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),  # Convert to int as M-Pesa requires whole numbers
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference[:12],  # M-Pesa limits this to 12 chars
            "TransactionDesc": transaction_desc[:13]  # M-Pesa limits this to 13 chars
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # In production, you might want to log this error
            raise Exception(f"Failed to initiate M-Pesa payment: {str(e)}")

    def check_payment_status(self, checkout_request_id):
        """
        Check the status of a payment
        """
        if not self.access_token:
            raise Exception("Access token not available")

        url = f"{self.base_url}/mpesa/stkpushquery/v1/query"

        # Generate password
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = f"{self.business_shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode("utf-8")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # In production, you might want to log this error
            raise Exception(f"Failed to check M-Pesa payment status: {str(e)}")