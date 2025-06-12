# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from .models import User, Room, Team, Booking
from .serializers import UserSerializer, RoomSerializer, TeamSerializer, BookingSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        current_time = now()
        booked_rooms = Booking.objects.filter(
            slot_start__lte=current_time,
            slot_end__gt=current_time
        ).values_list('room_id', flat=True)
        available_rooms = self.queryset.exclude(id__in=booked_rooms)
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def booked_rooms(self, request):
        bookings = self.queryset.select_related('room', 'user', 'team')
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
