# discounts/models.py

from django.db import models
from rooms.models import Room

class Discount(models.Model):
    discount_code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.discount_code

class RoomDiscount(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"Discount {self.discount.discount_code} for Room {self.room.room_number}"
