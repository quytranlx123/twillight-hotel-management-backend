# reviews/models.py

from django.db import models
from customers.models import Customer
from bookings.models import Booking

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    review_date = models.DateField()

    def __str__(self):
        return f"Review {self.id} by {self.customer}"
