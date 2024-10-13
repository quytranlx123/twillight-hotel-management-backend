import jwt
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed, NotFound
from .models import RoomType, Room
from .serializers import RoomSerializer, RoomTypeSerializer
from rest_framework.permissions import AllowAny


class RoomTypeListView(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người


class RoomTypeDetailView(generics.RetrieveAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người


class RoomTypeCreateView(generics.CreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người

    @csrf_exempt
    def perform_create(self, serializer):
        serializer.save()


class RoomTypeUpdateView(generics.UpdateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người

    def perform_update(self, serializer):
        serializer.save()


class RoomTypeDeleteView(generics.DestroyAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người

    def perform_destroy(self, instance):
        instance.delete()


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người


class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người

    def perform_create(self, serializer):
        serializer.save()


class RoomUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        # Lấy dữ liệu từ request
        data = self.request.data

        # Tạo một từ điển chứa các trường cần cập nhật
        update_fields = {}

        # Kiểm tra từng trường và chỉ thêm vào nếu không phải null
        for field in serializer.validated_data.keys():
            value = data.get(field, None)
            if value is not None:  # Nếu giá trị không phải là null
                if field == 'room_type':
                    # Chuyển đổi ID thành RoomType instance
                    try:
                        room_type_instance = RoomType.objects.get(id=value)
                        update_fields[field] = room_type_instance
                    except RoomType.DoesNotExist:
                        raise NotFound(f"RoomType with id {value} does not exist.")
                else:
                    update_fields[field] = value

        # Cập nhật chỉ các trường không phải null
        serializer.save(**update_fields)
        # Cập nhật chỉ các trường không phải


class RoomDeleteView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người

    def perform_destroy(self, instance):
        instance.delete()


class RoomListViewWithRoomType(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # Cho phép truy cập cho mọi người

    def get_queryset(self):
        queryset = Room.objects.all()
        room_type = self.request.query_params.get('room_type', None)
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        return queryset
