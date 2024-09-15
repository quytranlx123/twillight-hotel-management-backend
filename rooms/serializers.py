from rest_framework.serializers import ModelSerializer

from rooms.models import Room, RoomType


class RoomTypeSerializer(ModelSerializer):
    class Meta:
        model = RoomType
        fields = ["id", "type_name"]


class RoomSerializer(ModelSerializer):
    room_type = RoomTypeSerializer()

    class Meta:
        model = Room
        fields = ["id","room_number","room_type","status","price_per_night","room_type"]
