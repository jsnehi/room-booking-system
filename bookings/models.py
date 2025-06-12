import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Room(models.Model):
    ROOM_TYPES = [
        ('private', 'Private Room'),
        ('conference', 'Conference Room'),
        ('shared', 'Shared Desk'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField()
    total_rooms = models.PositiveIntegerField(default=1)
    booked = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.room_type == 'PRIVATE' and self.capacity != 1:
            raise ValidationError("Private rooms must have capacity=1")
        elif self.room_type == 'SHARED' and self.capacity != 4:
            raise ValidationError("Shared desks must have capacity=4")
    

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    @property
    def is_child(self):
        return self.age < 10
    
class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)

    @property
    def total_members(self):
        return self.members.count()

    @property
    def seating_required(self):
        return self.members.exclude(age__lt=10).count()
    
class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    slot_start = models.DateTimeField()
    slot_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Remove the condition-based constraint
            models.UniqueConstraint(
                fields=['room', 'slot_start'],
                name='unique_private_conference_booking'
            )
        ]

    def clean(self):
        # Validate booking constraints
        if self.room.room_type in ['PRIVATE', 'CONFERENCE']:
            existing = Booking.objects.filter(
                room=self.room,
                slot_start=self.slot_start
            ).exclude(pk=self.pk).exists()
            
            if existing:
                raise ValidationError(
                    "Private/Conference rooms can only have one booking per slot"
                )
        elif self.room.room_type == 'SHARED':
            existing = Booking.objects.filter(
                room=self.room,
                slot_start=self.slot_start
            ).count()
            if existing >= self.room.capacity:
                raise ValidationError("Shared desk slot full")

        # Check overlapping bookings
        overlapping = Booking.objects.filter(
            models.Q(user=self.user) | models.Q(team=self.team),
            slot_start__lt=self.slot_end,
            slot_end__gt=self.slot_start
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("User/team has overlapping booking")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        