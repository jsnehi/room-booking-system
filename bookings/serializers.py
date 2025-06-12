# serializers.py
from rest_framework import serializers
from .models import User, Room, Team, Booking

class UserSerializer(serializers.ModelSerializer):
    is_child = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'gender', 'is_child']

    def get_is_child(self, obj):
        return obj.is_child

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_type', 'capacity']

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'members', 'total_members', 'seating_required']
        read_only_fields = ['total_members', 'seating_required']

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        write_only=True, 
        required=False
    )
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), 
        source='team', 
        write_only=True, 
        required=False
    )
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), 
        source='room'
    )

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['created_at']
