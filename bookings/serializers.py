from rest_framework import serializers
from rooms.models import Room
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    room_code = serializers.CharField(write_only=True)  # Chỉ để ghi, không cần trả về
    check_in_date = serializers.DateTimeField(format='%d-%m-%Y')
    check_out_date = serializers.DateTimeField(format='%d-%m-%Y')
    room_name = serializers.CharField(source='room.name', read_only=True)  # Thêm trường room_name để trả về tên phòng
    room_type = serializers.CharField(source='room.room_type.room_type', read_only=True)
    price_per_night = serializers.CharField(source='room.room_type.price_per_night', read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        extra_kwargs = {
            'room': {'read_only': True}  # Tránh nhận trực tiếp khoá chính từ phía client
        }

    def validate(self, data):
        """
        Xác thực và tìm phòng dựa trên room_code.
        """
        room_code = data.pop('room_code', None)
        if room_code:
            try:
                room = Room.objects.get(name=room_code)
                data['room'] = room
            except Room.DoesNotExist:
                raise serializers.ValidationError(f"Phòng với mã {room_code} không tồn tại.")

        # Các kiểm tra khác liên quan đến khách hàng hoặc khách vãng lai
        if not data.get('customer') and not data.get('guest_firstname'):
            raise serializers.ValidationError("Cần cung cấp thông tin khách hàng hoặc thông tin khách vãng lai.")

        return data
