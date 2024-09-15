from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.parsers import MultiPartParser


class CustomUserViewSet(viewsets.ViewSet,
                      generics.ListCreateAPIView,
                      generics.CreateAPIView,
                      generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = CustomUserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]
