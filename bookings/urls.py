# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoomViewSet, TeamViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
