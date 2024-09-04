# otp/models.py

from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking
from payments.models import Invoice
from django.conf import settings


class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    otp_code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP {self.otp_code} for {self.user}"
