from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import RoomType, Room
from .serializers import RoomSerializer, RoomTypeSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(methods=['post'], detail=True, url_path='hide-rooms', url_name='hide-rooms')
    def hidden_room(self, request, pk):
        try:
            r = Room.objects.get(pk=pk)
            r.active = False
            r.save()
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=RoomSerializer(r).data, status=status.HTTP_200_OK)


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the room index.")
