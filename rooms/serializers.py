# serializers.py
from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'capacity', 'area', 'status', 'price_per_night', 'description',
                  'image', 'image_bathroom', 'image_amenities', 'created_at']
