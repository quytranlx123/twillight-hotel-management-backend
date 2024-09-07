from django.contrib import admin

from .models import RoomType, Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ["room_number", "room_type", "description", "status", "price_per_night"]
    search_fields = ["room_number", 'room_type__type_name', "description", "status", "price_per_night"]
    list_filter = ["status", 'room_type']


class RoomTypeInline(admin.StackedInline):
    model = Room
    max_num = 10
    pk_name = 'room_type'
    extra = 1


class RoomTypeAdmin(admin.ModelAdmin):
    inlines = (RoomTypeInline, )


admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
