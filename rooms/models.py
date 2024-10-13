from django.db import models
from django.utils.text import slugify


class RoomType(models.Model):
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
        ('4', '4 người'),
        ('6', '6 người'),
        ('8', '8 người')
    ]

    room_type = models.CharField(max_length=20, choices=ROOMTYPE_CHOICES, unique=True)
    capacity = models.CharField(max_length=20, choices=CAPACITY_CHOICES)
    area = models.FloatField()  # Diện tích (m²)
    price_per_night = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def upload_image_to(self, filename):
        # Sử dụng slugify để tạo một tên hợp lệ từ room_type
        return f'room_images/{slugify(self.room_type)}/{filename}'

    image = models.ImageField(upload_to=upload_image_to, null=True, blank=True)
    image_bathroom = models.ImageField(upload_to=upload_image_to, null=True, blank=True)
    image_amenities = models.ImageField(upload_to=upload_image_to, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.room_type


class Room(models.Model):
    STATUS_CHOICES = [
        ('trống', 'Trống'),
        ('đã đặt', 'Đã đặt'),
        ('đang bảo trì', 'Đang bảo trì'),
    ]

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trống')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
