from django.db import models


# rooms/models.py
# class RoomType(models.Model):
#     type_name = models.CharField(max_length=50)
#     description = models.TextField(null=True, blank=True)
#
#     def __str__(self):
#         return self.type_name

# Bảng phòng
class Room(models.Model):
    STATUS_CHOICES = [
        ('trống', 'Trống'),
        ('đã đặt', 'Đã đặt'),
        ('đang bảo trì', 'Đang bảo trì'),
    ]
    # Ocean View Room: 2, 25-35m2
    # Deluxe: 2-4, 30-50m2
    # Suite: 2-4, 50-80m2
    # Family: 4-6, 40-70m2
    # Resort: 2-4, 30-60m2
    # First Floor: 2-4, 25-45m2
    # Bungalow: 2-4, 50-100m2
    ROOMTYPE_CHOICES = [
        ('family', 'Family'),
        ('ground_floor', 'Ground Floor'),
        ('bungalow', 'Bungalow'),
        ('ocean_view', 'Ocean View Room'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
        ('resort', 'Resort'),
    ]
    CAPACITY_CHOICES = [
        ('2', '2 người'),
        ('2-4', '2-4 người'),
        ('4-6', '4-6 người'),
    ]
    name = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOMTYPE_CHOICES)
    capacity = models.CharField(max_length=20, choices=CAPACITY_CHOICES)
    area = models.FloatField()  # Diện tích (m²)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Trống')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name