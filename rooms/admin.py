from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "room_type", "capacity", "area", "price_per_night", "description","image", "status"]
    search_fields = ["description", "status", "price_per_night"]
    list_filter = ["status", 'room_type']
