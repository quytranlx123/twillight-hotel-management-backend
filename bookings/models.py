# bookings/models.py

from django.db import models
from customers.models import Customer
from rooms.models import Room
from discounts.models import Discount

class Booking(models.Model):
    STATUS_CHOICES = [
        ('đã đặt', 'Đã đặt'),
        ('đang ở', 'Đang ở'),
        ('đã hoàn thành', 'Đã hoàn thành'),
        ('đã hủy', 'Đã hủy'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Booking {self.id} for {self.customer}"
