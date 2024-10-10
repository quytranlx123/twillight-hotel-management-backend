from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk
import json

# Cấu hình PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # 'sandbox' hoặc 'live'
    "client_id": "AZ9Oe-xMLqgBcYyZI3B9IqULifMo2v43OIIqc8KIy811QqCU8upTB4wz_ORxrd0B3ssNeblBCyCQzqkJ",
    "client_secret": "EOpfFlz2UX4YHapC5LOu0EkIlKntR-fpwsjk3oqA2sK5vTjygDMt0kqEEk_ro32IJW6e6c56yyVSSHHM"
})

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:3000/success",
                "cancel_url": "http://localhost:3000/cancel"
            },
            "transactions": [{
                "amount": {
                    "total": "10.00",
                    "currency": "USD"
                },
                "description": "Mô tả thanh toán"
            }]
        })

        if payment.create():
            return JsonResponse(payment.to_dict())
        else:
            return JsonResponse({"error": payment.error}, status=500)
