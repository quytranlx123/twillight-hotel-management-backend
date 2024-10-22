# payments/models.py

from django.db import models
from bookings.models import Booking


# Bảng hoá đơn
class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('đã thanh toán', 'Đã thanh toán'),
        ('chưa thanh toán', 'Chưa thanh toán'),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)

    def __str__(self):
        return f"Invoice {self.id} for Booking {self.booking.id}"


# Bảng phương thức thanh toán
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('PayPal', 'PayPal'),
        ('Credit Card', 'Credit Card'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=50, unique=True)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.id} for Invoice {self.invoice.id}"


class PaymentTransaction(models.Model):
    app_trans_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
