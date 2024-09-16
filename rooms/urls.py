from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'room-types', views.RoomTypeViewSet)
urlpatterns = [
    path('', include(router.urls)),
]