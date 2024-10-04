# views.py
import jwt
from django.conf import settings
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from .models import Room
from .serializers import RoomSerializer


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


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager']:
            raise AuthenticationFailed('Permission denied')
        serializer.save()


class RoomUpdateView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_update(self, serializer):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager']:
            raise AuthenticationFailed('Permission denied')
        serializer.save()


class RoomDeleteView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_destroy(self, instance):
        role = self.authenticate(self.request)
        if role not in ['admin', 'manager']:
            raise AuthenticationFailed('Permission denied')
        instance.delete()
