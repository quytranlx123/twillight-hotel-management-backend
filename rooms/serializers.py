# serializers.py
from rest_framework import serializers
from .models import Room, RoomType


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'room_type', 'capacity', 'area', 'price_per_night', 'description',
                  'image', 'image_bathroom', 'image_amenities', 'created_at']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
