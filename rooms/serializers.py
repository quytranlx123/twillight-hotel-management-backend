# serializers.py
from rest_framework import serializers
from .models import Room, RoomType


from rest_framework import serializers

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id','room_type', 'capacity', 'area', 'price_per_night', 'description', 'image', 'image_bathroom', 'image_amenities']
        extra_kwargs = {
            'room_type': {'required': False},
            'capacity': {'required': False},
            'area': {'required': False},
            'price_per_night': {'required': False},
            'description': {'required': False},
            'image': {'required': False},
            'image_bathroom': {'required': False},
            'image_amenities': {'required': False},
        }


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
