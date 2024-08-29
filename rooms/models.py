from django.db import models
# rooms/models.py
class RoomType(models.Model):
    type_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.type_name


class Room(models.Model):
    STATUS_CHOICES = [
        ('trống', 'Trống'),
        ('đã đặt', 'Đã đặt'),
        ('đang bảo trì', 'Đang bảo trì'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.room_number
