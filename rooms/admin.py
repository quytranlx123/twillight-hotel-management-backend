from django.contrib import admin

from .models import Room, RoomType


@admin.register(RoomType)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', "room_type", "capacity", "area", "price_per_night", "description", "image"]
    search_fields = ["description", "price_per_night"]
    list_filter = ['room_type']
