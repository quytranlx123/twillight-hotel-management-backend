# promotions/models.py

from django.db import models
from bookings.models import Booking

class Promotion(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.code

class BookingPromotion(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Promotion {self.promotion.code} for Booking {self.booking.id}"
