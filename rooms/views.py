import jwt
from django.conf import settings
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from .models import RoomType, Room
from .serializers import RoomSerializer, RoomTypeSerializer


class RoomAuthenticationMixin:
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            role = payload.get('role')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token')

        return role


class RoomTypeListView(generics.ListAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomTypeDetailView(generics.RetrieveAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomTypeCreateView(RoomAuthenticationMixin, generics.CreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def perform_create(self, serializer):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager', 'employee']:
            raise AuthenticationFailed('Permission denied')
        serializer.save()


class RoomTypeUpdateView(RoomAuthenticationMixin, generics.UpdateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def perform_update(self, serializer):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager', 'employee']:
            raise AuthenticationFailed('Permission denied')
        serializer.save()


class RoomTypeDeleteView(RoomAuthenticationMixin, generics.DestroyAPIView):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

    def perform_destroy(self, instance):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager', 'employee']:
            raise AuthenticationFailed('Permission denied')
        instance.delete()


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomCreateView(RoomAuthenticationMixin, generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager', 'employee']:
            raise AuthenticationFailed('Permission denied')
        serializer.save()


class RoomUpdateView(RoomAuthenticationMixin, generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_update(self, serializer):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager', 'employee']:
            raise AuthenticationFailed('Permission denied')
        serializer.save()


class RoomDeleteView(RoomAuthenticationMixin, generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_destroy(self, instance):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager', 'employee']:
            raise AuthenticationFailed('Permission denied')
        instance.delete()


class RoomListViewWithRoomType(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()
        room_type = self.request.query_params.get('room_type', None)
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        return queryset
