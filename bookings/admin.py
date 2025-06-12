from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_type', 'capacity', 'total_rooms', 'booked']
    list_filter = ['room_type']
